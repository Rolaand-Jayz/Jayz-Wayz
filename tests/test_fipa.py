"""Tests for FIPA-ACL message support."""

import pytest
from datetime import datetime

from jayz_wayz.fipa import Message, Performative


def test_message_creation():
    """Test basic message creation."""
    msg = Message(
        performative=Performative.INFORM,
        sender="agent-1",
        receiver="agent-2",
        content={"text": "Hello"},
        conversation_id="conv-1"
    )
    
    assert msg.performative == Performative.INFORM
    assert msg.sender == "agent-1"
    assert msg.receiver == "agent-2"
    assert msg.content == {"text": "Hello"}
    assert msg.conversation_id == "conv-1"
    assert msg.protocol == "fipa-request"  # default
    assert msg.language == "json"  # default


def test_message_with_reply_to():
    """Test message with reply_to field."""
    msg = Message(
        performative=Performative.REQUEST,
        sender="user",
        receiver="agent",
        content={"action": "query"},
        conversation_id="conv-1",
        reply_to="msg-123"
    )
    
    assert msg.reply_to == "msg-123"


def test_message_to_dict():
    """Test message serialization to dict."""
    msg = Message(
        performative=Performative.PROPOSE,
        sender="agent",
        receiver="user",
        content={"proposal": "option A"},
        conversation_id="conv-1",
        message_id="msg-456"
    )
    
    msg_dict = msg.to_dict()
    
    assert msg_dict["performative"] == "propose"
    assert msg_dict["sender"] == "agent"
    assert msg_dict["receiver"] == "user"
    assert msg_dict["content"] == {"proposal": "option A"}
    assert msg_dict["conversation_id"] == "conv-1"
    assert msg_dict["message_id"] == "msg-456"
    assert isinstance(msg_dict["timestamp"], str)


def test_message_from_dict():
    """Test message deserialization from dict."""
    msg_dict = {
        "performative": "inform",
        "sender": "agent",
        "receiver": "user",
        "content": {"text": "Response"},
        "conversation_id": "conv-1",
        "reply_to": None,
        "protocol": "fipa-request",
        "language": "json",
        "ontology": None,
        "timestamp": "2024-01-01T12:00:00",
        "message_id": "msg-789",
        "metadata": {}
    }
    
    msg = Message.from_dict(msg_dict)
    
    assert msg.performative == Performative.INFORM
    assert msg.sender == "agent"
    assert msg.receiver == "user"
    assert msg.content == {"text": "Response"}
    assert msg.conversation_id == "conv-1"
    assert msg.message_id == "msg-789"
    assert isinstance(msg.timestamp, datetime)


def test_message_create_reply():
    """Test creating a reply message."""
    original = Message(
        performative=Performative.REQUEST,
        sender="user",
        receiver="agent",
        content={"query": "status"},
        conversation_id="conv-1",
        message_id="msg-100"
    )
    
    reply = original.create_reply(
        performative=Performative.INFORM,
        content={"status": "active"},
        sender="agent"
    )
    
    assert reply.performative == Performative.INFORM
    assert reply.sender == "agent"
    assert reply.receiver == "user"  # Flipped
    assert reply.conversation_id == "conv-1"  # Preserved
    assert reply.reply_to == "msg-100"
    assert reply.protocol == "fipa-request"  # Inherited
    assert reply.content == {"status": "active"}


def test_performative_enum():
    """Test performative enum values."""
    assert Performative.INFORM.value == "inform"
    assert Performative.REQUEST.value == "request"
    assert Performative.QUERY.value == "query"
    assert Performative.ACCEPT.value == "accept"
    assert Performative.REJECT.value == "reject"
    assert Performative.FAILURE.value == "failure"


def test_message_with_metadata():
    """Test message with custom metadata."""
    msg = Message(
        performative=Performative.INFORM,
        sender="agent",
        receiver="user",
        content={"text": "test"},
        conversation_id="conv-1",
        metadata={"priority": "high", "tags": ["urgent"]}
    )
    
    assert msg.metadata["priority"] == "high"
    assert msg.metadata["tags"] == ["urgent"]


def test_message_with_ontology():
    """Test message with ontology specification."""
    msg = Message(
        performative=Performative.QUERY,
        sender="agent",
        receiver="service",
        content={"entity": "user123"},
        conversation_id="conv-1",
        ontology="user-management-v1"
    )
    
    assert msg.ontology == "user-management-v1"


def test_message_roundtrip_serialization():
    """Test that message survives serialization roundtrip."""
    original = Message(
        performative=Performative.CONFIRM,
        sender="agent-a",
        receiver="agent-b",
        content={"confirmed": True, "details": {"count": 42}},
        conversation_id="conv-roundtrip",
        reply_to="prev-msg",
        protocol="custom-protocol",
        language="json",
        ontology="test-ontology",
        message_id="msg-roundtrip",
        metadata={"key": "value"}
    )
    
    # Serialize
    msg_dict = original.to_dict()
    
    # Deserialize
    restored = Message.from_dict(msg_dict)
    
    # Verify all fields preserved
    assert restored.performative == original.performative
    assert restored.sender == original.sender
    assert restored.receiver == original.receiver
    assert restored.content == original.content
    assert restored.conversation_id == original.conversation_id
    assert restored.reply_to == original.reply_to
    assert restored.protocol == original.protocol
    assert restored.language == original.language
    assert restored.ontology == original.ontology
    assert restored.message_id == original.message_id
    assert restored.metadata == original.metadata
