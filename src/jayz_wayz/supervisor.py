"""Supervisor (Jayz Wayz) facade integrating runner, PEP, and checkpointing."""

import asyncio
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from .langgraph_core import AsyncGraphRunner, RunnerConfig
from .state import GraphState
from .checkpoint import CheckpointStore
from .policy import PolicyEnforcer, CompositePolicyEnforcer, OPAHttpPolicyEnforcer, LocalDenyEnforcer
from .nodes import create_greeting_node, create_processing_node, finalize_node


class Supervisor:
    """Jayz Wayz - Supervisor facade that integrates all Phase 1 components.
    
    The Supervisor coordinates:
    - Async graph execution via AsyncGraphRunner
    - Policy enforcement via PolicyEnforcer
    - State checkpointing via CheckpointStore
    
    Attributes:
        runner: Async graph runner
        policy_enforcer: Policy enforcement point
        checkpoint_store: Checkpoint storage
    """
    
    def __init__(
        self,
        runner_config: Optional[RunnerConfig] = None,
        policy_enforcer: Optional[PolicyEnforcer] = None,
        checkpoint_dir: str = "checkpoints",
        enable_opa: bool = False,
        opa_url: str = "http://localhost:8181"
    ):
        """Initialize the Supervisor.
        
        Args:
            runner_config: Configuration for the async runner
            policy_enforcer: Optional custom policy enforcer
            checkpoint_dir: Directory for checkpoints
            enable_opa: Whether to enable OPA HTTP enforcer
            opa_url: OPA server URL if enabled
        """
        self.runner = AsyncGraphRunner(runner_config or RunnerConfig())
        
        # Setup policy enforcer with fallback
        if policy_enforcer:
            self.policy_enforcer = policy_enforcer
        elif enable_opa:
            primary = OPAHttpPolicyEnforcer(opa_url=opa_url)
            fallback = LocalDenyEnforcer()
            self.policy_enforcer = CompositePolicyEnforcer(primary, fallback)
        else:
            # Use local deny enforcer by default for safety
            self.policy_enforcer = LocalDenyEnforcer()
        
        self.checkpoint_store = CheckpointStore(checkpoint_dir)
    
    async def enforce_policy(
        self,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if an action is allowed by policy.
        
        Args:
            action: Action to check (e.g., 'execute', 'read', 'write')
            resource: Resource being accessed
            context: Additional context for decision
            
        Returns:
            True if allowed, False otherwise
        """
        return await self.policy_enforcer.enforce(action, resource, context)
    
    def save_checkpoint(
        self,
        state: GraphState,
        checkpoint_id: Optional[str] = None
    ) -> str:
        """Save a checkpoint of the current state.
        
        Args:
            state: Current graph state
            checkpoint_id: Optional checkpoint ID (generated if not provided)
            
        Returns:
            Checkpoint ID
        """
        checkpoint_id = checkpoint_id or f"{state.conversation_id}_{uuid4().hex[:8]}"
        
        metadata = {
            "conversation_id": state.conversation_id,
            "current_step": state.current_step,
            "message_count": len(state.messages)
        }
        
        self.checkpoint_store.save(checkpoint_id, state.to_dict(), metadata)
        return checkpoint_id
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[GraphState]:
        """Load a checkpoint and restore state.
        
        Args:
            checkpoint_id: ID of checkpoint to load
            
        Returns:
            Restored state, or None if not found
        """
        checkpoint_data = self.checkpoint_store.load(checkpoint_id)
        if not checkpoint_data:
            return None
        
        state_dict = checkpoint_data.get("state", {})
        return GraphState.from_dict(state_dict)
    
    def list_checkpoints(
        self,
        conversation_id: Optional[str] = None
    ) -> list[Dict[str, Any]]:
        """List all checkpoints.
        
        Args:
            conversation_id: Optional filter by conversation
            
        Returns:
            List of checkpoint metadata
        """
        return self.checkpoint_store.list_checkpoints(conversation_id)
    
    def rollback_to_checkpoint(self, checkpoint_id: str) -> Optional[GraphState]:
        """Rollback to a specific checkpoint.
        
        Args:
            checkpoint_id: ID of checkpoint to rollback to
            
        Returns:
            Restored state, or None if not found
        """
        state_dict = self.checkpoint_store.rollback(checkpoint_id)
        if not state_dict:
            return None
        
        return GraphState.from_dict(state_dict)
    
    async def run_conversation(
        self,
        conversation_id: str,
        custom_nodes: Optional[Dict[str, Callable[[GraphState], GraphState]]] = None,
        auto_checkpoint: bool = True
    ) -> GraphState:
        """Run a complete conversation workflow.
        
        Args:
            conversation_id: Unique conversation identifier
            custom_nodes: Optional custom node definitions
            auto_checkpoint: Whether to auto-save checkpoints
            
        Returns:
            Final conversation state
        """
        # Check policy for executing conversation
        allowed = await self.enforce_policy(
            action="execute",
            resource=f"conversation/{conversation_id}",
            context={"conversation_id": conversation_id}
        )
        
        if not allowed:
            # Create error state
            state = GraphState(conversation_id=conversation_id)
            state.error = "Policy denied conversation execution"
            return state
        
        # Initialize state
        initial_state = GraphState(conversation_id=conversation_id)
        
        # Define default conversation workflow
        if custom_nodes is None:
            nodes = {
                "greeting": create_greeting_node(),
                "processing": create_processing_node(),
                "finalize": finalize_node()
            }
        else:
            nodes = custom_nodes
        
        # Run the graph
        final_state = await self.runner.run_graph(
            nodes=nodes,
            initial_state=initial_state,
            node_order=list(nodes.keys())
        )
        
        # Auto-checkpoint if enabled and no errors
        if auto_checkpoint and not final_state.error:
            checkpoint_id = self.save_checkpoint(final_state)
            final_state.add_checkpoint(checkpoint_id)
        
        return final_state
    
    async def close(self) -> None:
        """Close resources (e.g., HTTP sessions)."""
        if isinstance(self.policy_enforcer, CompositePolicyEnforcer):
            if hasattr(self.policy_enforcer.primary, 'close'):
                await self.policy_enforcer.primary.close()
