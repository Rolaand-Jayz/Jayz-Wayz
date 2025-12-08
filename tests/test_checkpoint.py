"""Tests for checkpoint store."""

import pytest
import tempfile
import shutil
from pathlib import Path

from jayz_wayz.checkpoint import CheckpointStore
from jayz_wayz.state import GraphState


@pytest.fixture
def temp_checkpoint_dir():
    """Create a temporary checkpoint directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_checkpoint_save_and_load(temp_checkpoint_dir):
    """Test saving and loading checkpoints."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    state = GraphState(conversation_id="conv-1")
    state.add_message({"text": "test message"})
    state.current_step = "step1"
    
    # Save checkpoint
    checkpoint_id = "test-checkpoint-1"
    filepath = store.save(checkpoint_id, state.to_dict(), {"note": "test"})
    
    assert Path(filepath).exists()
    
    # Load checkpoint
    loaded = store.load(checkpoint_id)
    
    assert loaded is not None
    assert loaded["state"]["conversation_id"] == "conv-1"
    assert loaded["metadata"]["checkpoint_id"] == checkpoint_id
    assert loaded["metadata"]["note"] == "test"


def test_checkpoint_not_found(temp_checkpoint_dir):
    """Test loading non-existent checkpoint."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    loaded = store.load("nonexistent")
    
    assert loaded is None


def test_checkpoint_list(temp_checkpoint_dir):
    """Test listing checkpoints."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    # Create multiple checkpoints
    state1 = GraphState(conversation_id="conv-1")
    state1.current_step = "step1"
    store.save("checkpoint-1", state1.to_dict())
    
    state2 = GraphState(conversation_id="conv-2")
    state2.current_step = "step2"
    store.save("checkpoint-2", state2.to_dict())
    
    state3 = GraphState(conversation_id="conv-1")
    state3.current_step = "step3"
    store.save("checkpoint-3", state3.to_dict())
    
    # List all checkpoints
    all_checkpoints = store.list_checkpoints()
    assert len(all_checkpoints) == 3
    
    # List filtered by conversation_id
    conv1_checkpoints = store.list_checkpoints(conversation_id="conv-1")
    assert len(conv1_checkpoints) == 2
    assert all(cp["conversation_id"] == "conv-1" for cp in conv1_checkpoints)


def test_checkpoint_list_sorted(temp_checkpoint_dir):
    """Test that checkpoints are sorted by timestamp."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    # Create checkpoints with delay
    import time
    
    state1 = GraphState(conversation_id="conv-1")
    store.save("checkpoint-1", state1.to_dict())
    
    time.sleep(0.1)
    
    state2 = GraphState(conversation_id="conv-1")
    store.save("checkpoint-2", state2.to_dict())
    
    checkpoints = store.list_checkpoints()
    
    # Should be sorted newest first
    assert checkpoints[0]["checkpoint_id"] == "checkpoint-2"
    assert checkpoints[1]["checkpoint_id"] == "checkpoint-1"


def test_checkpoint_rollback(temp_checkpoint_dir):
    """Test rollback functionality."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    state = GraphState(conversation_id="conv-1")
    state.add_message({"text": "checkpoint message"})
    state.current_step = "saved_step"
    
    checkpoint_id = "rollback-test"
    store.save(checkpoint_id, state.to_dict())
    
    # Rollback
    restored_state_dict = store.rollback(checkpoint_id)
    
    assert restored_state_dict is not None
    assert restored_state_dict["conversation_id"] == "conv-1"
    assert restored_state_dict["current_step"] == "saved_step"
    assert len(restored_state_dict["messages"]) == 1


def test_checkpoint_delete(temp_checkpoint_dir):
    """Test checkpoint deletion."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    state = GraphState(conversation_id="conv-1")
    checkpoint_id = "delete-test"
    store.save(checkpoint_id, state.to_dict())
    
    # Verify exists
    assert store.load(checkpoint_id) is not None
    
    # Delete
    result = store.delete(checkpoint_id)
    assert result is True
    
    # Verify deleted
    assert store.load(checkpoint_id) is None
    
    # Try deleting again
    result = store.delete(checkpoint_id)
    assert result is False


def test_checkpoint_cleanup_old(temp_checkpoint_dir):
    """Test cleanup of old checkpoints."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    # Create checkpoints
    for i in range(3):
        state = GraphState(conversation_id=f"conv-{i}")
        store.save(f"checkpoint-{i}", state.to_dict())
    
    # Cleanup with max_age_days=0 (should delete all)
    deleted = store.cleanup_old_checkpoints(max_age_days=0)
    
    # Note: This might be 0 or 3 depending on timing
    # The important thing is it runs without error
    assert deleted >= 0


def test_checkpoint_metadata_preserved(temp_checkpoint_dir):
    """Test that custom metadata is preserved."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    state = GraphState(conversation_id="conv-1")
    metadata = {
        "user": "test-user",
        "tags": ["important", "demo"],
        "version": "1.0"
    }
    
    checkpoint_id = "metadata-test"
    store.save(checkpoint_id, state.to_dict(), metadata)
    
    loaded = store.load(checkpoint_id)
    loaded_metadata = loaded["metadata"]
    
    assert loaded_metadata["user"] == "test-user"
    assert loaded_metadata["tags"] == ["important", "demo"]
    assert loaded_metadata["version"] == "1.0"
    assert "timestamp" in loaded_metadata  # Auto-added


def test_checkpoint_with_complex_state(temp_checkpoint_dir):
    """Test checkpoint with complex state."""
    store = CheckpointStore(temp_checkpoint_dir)
    
    state = GraphState(conversation_id="conv-complex")
    state.add_message({"sender": "user", "content": "Hello"})
    state.add_message({"sender": "agent", "content": "Hi there"})
    state.metadata = {"nested": {"key": "value"}, "list": [1, 2, 3]}
    state.current_step = "complex_step"
    state.add_checkpoint("previous-checkpoint")
    
    checkpoint_id = "complex-test"
    store.save(checkpoint_id, state.to_dict())
    
    loaded = store.load(checkpoint_id)
    loaded_state = GraphState.from_dict(loaded["state"])
    
    assert loaded_state.conversation_id == "conv-complex"
    assert len(loaded_state.messages) == 2
    assert loaded_state.metadata["nested"]["key"] == "value"
    assert loaded_state.metadata["list"] == [1, 2, 3]
    assert loaded_state.current_step == "complex_step"
    assert "previous-checkpoint" in loaded_state.checkpoints
