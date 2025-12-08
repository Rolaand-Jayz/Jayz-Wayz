"""FIPA-ACL (Foundation for Intelligent Physical Agents - Agent Communication Language) message support."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class Performative(Enum):
    """FIPA-ACL performative types."""
    INFORM = "inform"
    REQUEST = "request"
    QUERY = "query"
    PROPOSE = "propose"
    ACCEPT = "accept"
    REJECT = "reject"
    CONFIRM = "confirm"
    DISCONFIRM = "disconfirm"
    FAILURE = "failure"
    AGREE = "agree"
    REFUSE = "refuse"


@dataclass
class Message:
    """FIPA-ACL compliant message structure.
    
    Attributes:
        performative: Type of communicative act
        sender: Agent identifier of the sender
        receiver: Agent identifier of the receiver
        content: Message content (can be any serializable data)
        conversation_id: Identifier linking related messages
        reply_to: Message ID this is replying to
        protocol: Interaction protocol being used
        language: Content language (e.g., 'json', 'text')
        ontology: Ontology/schema for content interpretation
        timestamp: When the message was created
        message_id: Unique identifier for this message
        metadata: Additional metadata
    """
    performative: Performative
    sender: str
    receiver: str
    content: Any
    conversation_id: str
    reply_to: Optional[str] = None
    protocol: str = "fipa-request"
    language: str = "json"
    ontology: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    message_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        data = asdict(self)
        data["performative"] = self.performative.value
        data["timestamp"] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary."""
        data = data.copy()
        data["performative"] = Performative(data["performative"])
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)
    
    def create_reply(
        self,
        performative: Performative,
        content: Any,
        sender: str,
        **kwargs: Any
    ) -> "Message":
        """Create a reply to this message."""
        return Message(
            performative=performative,
            sender=sender,
            receiver=self.sender,
            content=content,
            conversation_id=self.conversation_id,
            reply_to=self.message_id,
            protocol=self.protocol,
            **kwargs
        )
