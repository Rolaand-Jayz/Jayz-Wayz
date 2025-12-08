"""Tests for async graph runner."""

import asyncio
import pytest

from jayz_wayz.langgraph_core import AsyncGraphRunner, RunnerConfig
from jayz_wayz.state import GraphState


@pytest.mark.asyncio
async def test_runner_basic_execution():
    """Test basic graph execution."""
    runner = AsyncGraphRunner()
    
    def node1(state: GraphState) -> GraphState:
        state.metadata["visited"] = state.metadata.get("visited", [])
        state.metadata["visited"].append("node1")
        return state
    
    def node2(state: GraphState) -> GraphState:
        state.metadata["visited"] = state.metadata.get("visited", [])
        state.metadata["visited"].append("node2")
        return state
    
    initial_state = GraphState(conversation_id="test-1")
    
    nodes = {"node1": node1, "node2": node2}
    final_state = await runner.run_graph(nodes, initial_state, ["node1", "node2"])
    
    assert final_state.conversation_id == "test-1"
    assert final_state.metadata["visited"] == ["node1", "node2"]
    assert final_state.error is None


@pytest.mark.asyncio
async def test_runner_async_node():
    """Test execution with async node."""
    runner = AsyncGraphRunner()
    
    async def async_node(state: GraphState) -> GraphState:
        await asyncio.sleep(0.01)
        state.metadata["async_executed"] = True
        return state
    
    initial_state = GraphState(conversation_id="test-2")
    
    final_state = await runner.run_node(async_node, initial_state, "async_node")
    
    assert final_state.metadata["async_executed"] is True
    assert final_state.current_step == "async_node"


@pytest.mark.asyncio
async def test_runner_timeout():
    """Test timeout handling."""
    config = RunnerConfig(timeout=1, max_retries=1)
    runner = AsyncGraphRunner(config)
    
    async def slow_node(state: GraphState) -> GraphState:
        await asyncio.sleep(2)  # Longer than timeout
        return state
    
    initial_state = GraphState(conversation_id="test-3")
    
    with pytest.raises(asyncio.TimeoutError):
        await runner.run_node(slow_node, initial_state, "slow_node")


@pytest.mark.asyncio
async def test_runner_retry_success():
    """Test retry mechanism with eventual success."""
    config = RunnerConfig(timeout=5, max_retries=3, retry_delay=0.1)
    runner = AsyncGraphRunner(config)
    
    attempt_count = {"count": 0}
    
    def flaky_node(state: GraphState) -> GraphState:
        attempt_count["count"] += 1
        if attempt_count["count"] < 2:
            raise ValueError("Temporary failure")
        state.metadata["attempts"] = attempt_count["count"]
        return state
    
    initial_state = GraphState(conversation_id="test-4")
    
    final_state = await runner.run_node(flaky_node, initial_state, "flaky_node")
    
    assert final_state.metadata["attempts"] == 2
    assert final_state.error is None


@pytest.mark.asyncio
async def test_runner_retry_exhausted():
    """Test retry exhaustion."""
    config = RunnerConfig(timeout=5, max_retries=2, retry_delay=0.1)
    runner = AsyncGraphRunner(config)
    
    def failing_node(state: GraphState) -> GraphState:
        raise ValueError("Permanent failure")
    
    initial_state = GraphState(conversation_id="test-5")
    
    with pytest.raises(ValueError):
        await runner.run_node(failing_node, initial_state, "failing_node")


@pytest.mark.asyncio
async def test_runner_conditional():
    """Test conditional execution."""
    runner = AsyncGraphRunner()
    
    def condition(state: GraphState) -> bool:
        return state.metadata.get("flag", False)
    
    def true_node(state: GraphState) -> GraphState:
        state.metadata["branch"] = "true"
        return state
    
    def false_node(state: GraphState) -> GraphState:
        state.metadata["branch"] = "false"
        return state
    
    # Test false branch
    state1 = GraphState(conversation_id="test-6")
    result1 = await runner.run_conditional(condition, true_node, false_node, state1)
    assert result1.metadata["branch"] == "false"
    
    # Test true branch
    state2 = GraphState(conversation_id="test-7")
    state2.metadata["flag"] = True
    result2 = await runner.run_conditional(condition, true_node, false_node, state2)
    assert result2.metadata["branch"] == "true"


@pytest.mark.asyncio
async def test_runner_error_propagation():
    """Test that errors stop graph execution."""
    runner = AsyncGraphRunner()
    
    def node1(state: GraphState) -> GraphState:
        state.metadata["node1"] = True
        return state
    
    def error_node(state: GraphState) -> GraphState:
        raise RuntimeError("Intentional error")
    
    def node3(state: GraphState) -> GraphState:
        state.metadata["node3"] = True
        return state
    
    initial_state = GraphState(conversation_id="test-8")
    
    nodes = {"node1": node1, "error_node": error_node, "node3": node3}
    
    final_state = await runner.run_graph(nodes, initial_state, ["node1", "error_node", "node3"])
    
    assert final_state.metadata.get("node1") is True
    assert final_state.metadata.get("node3") is None  # Should not execute
    assert final_state.error is not None
    assert "error_node" in final_state.error
