"""State management for Jayz Wayz graphs."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GraphState:
    """State for the Jayz Wayz graph execution.
    
    Attributes:
        conversation_id: Unique identifier for the conversation
        messages: List of FIPA-ACL messages exchanged
        metadata: Additional metadata for the conversation
        checkpoints: List of checkpoint IDs for this conversation
        current_step: Current step in the graph execution
        error: Error message if execution failed
    """
    conversation_id: str
    messages: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    checkpoints: List[str] = field(default_factory=list)
    current_step: Optional[str] = None
    error: Optional[str] = None
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to the conversation history."""
        self.messages.append(message)
    
    def add_checkpoint(self, checkpoint_id: str) -> None:
        """Record a checkpoint for this conversation."""
        self.checkpoints.append(checkpoint_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "conversation_id": self.conversation_id,
            "messages": self.messages,
            "metadata": self.metadata,
            "checkpoints": self.checkpoints,
            "current_step": self.current_step,
            "error": self.error,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphState":
        """Create state from dictionary."""
        return cls(
            conversation_id=data["conversation_id"],
            messages=data.get("messages", []),
            metadata=data.get("metadata", {}),
            checkpoints=data.get("checkpoints", []),
            current_step=data.get("current_step"),
            error=data.get("error"),
        )
