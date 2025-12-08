"""Async graph runner with timeout and retry behavior."""

import asyncio
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass

from .state import GraphState


@dataclass
class RunnerConfig:
    """Configuration for the async graph runner.
    
    Attributes:
        timeout: Maximum execution time in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    """
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0


class AsyncGraphRunner:
    """Async graph execution runner with timeout and retry support.
    
    This runner executes graph nodes asynchronously with configurable
    timeout and retry behavior.
    """
    
    def __init__(self, config: Optional[RunnerConfig] = None):
        """Initialize the async runner.
        
        Args:
            config: Runner configuration
        """
        self.config = config or RunnerConfig()
    
    async def run_node(
        self,
        node_func: Callable[[GraphState], GraphState],
        state: GraphState,
        node_name: str
    ) -> GraphState:
        """Run a single node with timeout and retry.
        
        Args:
            node_func: The node function to execute
            state: Current graph state
            node_name: Name of the node for logging
            
        Returns:
            Updated graph state
            
        Raises:
            asyncio.TimeoutError: If node execution times out
            Exception: If node fails after all retries
        """
        state.current_step = node_name
        
        for attempt in range(self.config.max_retries):
            try:
                # Run node with timeout
                result = await asyncio.wait_for(
                    self._execute_node(node_func, state),
                    timeout=self.config.timeout
                )
                return result
            except asyncio.TimeoutError:
                if attempt == self.config.max_retries - 1:
                    state.error = f"Node '{node_name}' timed out after {self.config.timeout}s"
                    raise
                await asyncio.sleep(self.config.retry_delay)
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    state.error = f"Node '{node_name}' failed: {str(e)}"
                    raise
                await asyncio.sleep(self.config.retry_delay)
        
        return state
    
    async def _execute_node(
        self,
        node_func: Callable[[GraphState], GraphState],
        state: GraphState
    ) -> GraphState:
        """Execute a node function (potentially async or sync).
        
        Args:
            node_func: The node function to execute
            state: Current graph state
            
        Returns:
            Updated graph state
        """
        if asyncio.iscoroutinefunction(node_func):
            return await node_func(state)
        else:
            # Run sync function in executor to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, node_func, state)
    
    async def run_graph(
        self,
        nodes: Dict[str, Callable[[GraphState], GraphState]],
        initial_state: GraphState,
        node_order: Optional[list[str]] = None
    ) -> GraphState:
        """Run a complete graph of nodes.
        
        Args:
            nodes: Dictionary mapping node names to functions
            initial_state: Initial graph state
            node_order: Optional list specifying node execution order
            
        Returns:
            Final graph state after all nodes execute
        """
        state = initial_state
        order = node_order or list(nodes.keys())
        
        for node_name in order:
            if node_name not in nodes:
                state.error = f"Node '{node_name}' not found in graph"
                break
            
            if state.error:
                # Stop execution if previous node had an error
                break
            
            try:
                state = await self.run_node(nodes[node_name], state, node_name)
            except Exception as e:
                # Error already set in run_node
                break
        
        return state
    
    async def run_conditional(
        self,
        condition_func: Callable[[GraphState], bool],
        true_node: Callable[[GraphState], GraphState],
        false_node: Callable[[GraphState], GraphState],
        state: GraphState,
        node_name: str = "conditional"
    ) -> GraphState:
        """Run conditional execution based on state.
        
        Args:
            condition_func: Function to evaluate condition
            true_node: Node to execute if condition is True
            false_node: Node to execute if condition is False
            state: Current graph state
            node_name: Name for this conditional node
            
        Returns:
            Updated graph state
        """
        try:
            # Evaluate condition
            if asyncio.iscoroutinefunction(condition_func):
                condition = await condition_func(state)
            else:
                loop = asyncio.get_event_loop()
                condition = await loop.run_in_executor(None, condition_func, state)
            
            # Execute appropriate branch
            selected_node = true_node if condition else false_node
            branch_name = f"{node_name}_true" if condition else f"{node_name}_false"
            
            return await self.run_node(selected_node, state, branch_name)
        except Exception as e:
            state.error = f"Conditional '{node_name}' failed: {str(e)}"
            return state
