"""Enhanced checkpoint store with metadata, list, and rollback capabilities."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class CheckpointStore:
    """Enhanced checkpoint storage with metadata and rollback support.
    
    Attributes:
        checkpoint_dir: Directory where checkpoints are stored
    """
    
    def __init__(self, checkpoint_dir: str = "checkpoints"):
        """Initialize checkpoint store.
        
        Args:
            checkpoint_dir: Directory for storing checkpoints
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
    
    def save(
        self,
        checkpoint_id: str,
        state: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save a checkpoint with metadata.
        
        Args:
            checkpoint_id: Unique identifier for the checkpoint
            state: State data to checkpoint
            metadata: Additional metadata about the checkpoint
            
        Returns:
            Path to the saved checkpoint file
        """
        metadata = metadata or {}
        metadata["timestamp"] = datetime.now(timezone.utc).isoformat()
        metadata["checkpoint_id"] = checkpoint_id
        
        checkpoint_data = {
            "state": state,
            "metadata": metadata
        }
        
        filepath = self.checkpoint_dir / f"{checkpoint_id}.json"
        with open(filepath, "w") as f:
            json.dump(checkpoint_data, f, indent=2)
        
        return str(filepath)
    
    def load(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Load a checkpoint by ID.
        
        Args:
            checkpoint_id: Unique identifier for the checkpoint
            
        Returns:
            Checkpoint data including state and metadata, or None if not found
        """
        filepath = self.checkpoint_dir / f"{checkpoint_id}.json"
        if not filepath.exists():
            return None
        
        with open(filepath, "r") as f:
            return json.load(f)
    
    def list_checkpoints(
        self,
        conversation_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all checkpoints, optionally filtered by conversation ID.
        
        Args:
            conversation_id: Filter checkpoints by conversation ID
            
        Returns:
            List of checkpoint metadata
        """
        checkpoints = []
        
        for filepath in self.checkpoint_dir.glob("*.json"):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    metadata = data.get("metadata", {})
                    
                    # Filter by conversation_id if provided
                    if conversation_id:
                        state = data.get("state", {})
                        if state.get("conversation_id") != conversation_id:
                            continue
                    
                    checkpoints.append({
                        "checkpoint_id": metadata.get("checkpoint_id", filepath.stem),
                        "timestamp": metadata.get("timestamp"),
                        "conversation_id": data.get("state", {}).get("conversation_id"),
                        "current_step": data.get("state", {}).get("current_step"),
                        "metadata": metadata
                    })
            except (json.JSONDecodeError, IOError):
                continue
        
        # Sort by timestamp, newest first
        checkpoints.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return checkpoints
    
    def rollback(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Rollback to a specific checkpoint.
        
        Args:
            checkpoint_id: ID of checkpoint to rollback to
            
        Returns:
            The restored state, or None if checkpoint not found
        """
        checkpoint_data = self.load(checkpoint_id)
        if not checkpoint_data:
            return None
        
        return checkpoint_data.get("state")
    
    def delete(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint.
        
        Args:
            checkpoint_id: ID of checkpoint to delete
            
        Returns:
            True if deleted, False if not found
        """
        filepath = self.checkpoint_dir / f"{checkpoint_id}.json"
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    def cleanup_old_checkpoints(self, max_age_days: int = 30) -> int:
        """Remove checkpoints older than specified days.
        
        Args:
            max_age_days: Maximum age of checkpoints to keep
            
        Returns:
            Number of checkpoints deleted
        """
        deleted_count = 0
        cutoff_time = datetime.now(timezone.utc).timestamp() - (max_age_days * 86400)
        
        for filepath in self.checkpoint_dir.glob("*.json"):
            try:
                mtime = filepath.stat().st_mtime
                if mtime < cutoff_time:
                    filepath.unlink()
                    deleted_count += 1
            except OSError:
                continue
        
        return deleted_count
