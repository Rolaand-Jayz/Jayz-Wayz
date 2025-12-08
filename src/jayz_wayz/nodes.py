"""Async node wrappers and common node implementations."""

import asyncio
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from .state import GraphState
from .fipa import Message, Performative


async def async_node_wrapper(
    func: Callable[[GraphState], GraphState],
    state: GraphState
) -> GraphState:
    """Wrap a sync node function to run asynchronously.
    
    Args:
        func: Sync node function
        state: Current state
        
    Returns:
        Updated state
    """
    if asyncio.iscoroutinefunction(func):
        return await func(state)
    else:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, state)


def create_greeting_node() -> Callable[[GraphState], GraphState]:
    """Create a node that sends a greeting message.
    
    Returns:
        Node function that adds a greeting message
    """
    def greeting_node(state: GraphState) -> GraphState:
        """Send greeting message."""
        message = Message(
            performative=Performative.INFORM,
            sender="jayz-wayz",
            receiver="user",
            content={"text": f"Hello! Starting conversation {state.conversation_id}"},
            conversation_id=state.conversation_id,
            message_id=str(uuid4())
        )
        state.add_message(message.to_dict())
        return state
    
    return greeting_node


def create_processing_node(
    process_func: Optional[Callable[[str], str]] = None
) -> Callable[[GraphState], GraphState]:
    """Create a node that processes messages.
    
    Args:
        process_func: Optional custom processing function
        
    Returns:
        Node function that processes the latest message
    """
    def default_process(content: str) -> str:
        """Default processing: echo with prefix."""
        return f"Processed: {content}"
    
    processor = process_func or default_process
    
    def processing_node(state: GraphState) -> GraphState:
        """Process the latest message."""
        if state.messages:
            last_msg = state.messages[-1]
            content = last_msg.get("content", {})
            
            if isinstance(content, dict) and "text" in content:
                processed_text = processor(content["text"])
                
                response = Message(
                    performative=Performative.INFORM,
                    sender="jayz-wayz",
                    receiver=last_msg.get("sender", "user"),
                    content={"text": processed_text},
                    conversation_id=state.conversation_id,
                    reply_to=last_msg.get("message_id"),
                    message_id=str(uuid4())
                )
                state.add_message(response.to_dict())
        
        return state
    
    return processing_node


def create_checkpoint_node(
    checkpoint_func: Callable[[GraphState], str]
) -> Callable[[GraphState], GraphState]:
    """Create a node that saves checkpoints.
    
    Args:
        checkpoint_func: Function that takes state and returns checkpoint ID
        
    Returns:
        Node function that saves a checkpoint
    """
    def checkpoint_node(state: GraphState) -> GraphState:
        """Save checkpoint for current state."""
        checkpoint_id = checkpoint_func(state)
        state.add_checkpoint(checkpoint_id)
        return state
    
    return checkpoint_node


async def validate_node(state: GraphState) -> GraphState:
    """Example async node that validates the state.
    
    Args:
        state: Current state
        
    Returns:
        Updated state with validation result
    """
    # Simulate async validation
    await asyncio.sleep(0.1)
    
    if not state.conversation_id:
        state.error = "Missing conversation_id"
    
    return state


def error_handler_node(state: GraphState) -> GraphState:
    """Node that handles errors.
    
    Args:
        state: Current state
        
    Returns:
        State with error message added to messages
    """
    if state.error:
        error_msg = Message(
            performative=Performative.FAILURE,
            sender="jayz-wayz",
            receiver="user",
            content={"error": state.error},
            conversation_id=state.conversation_id,
            message_id=str(uuid4())
        )
        state.add_message(error_msg.to_dict())
    
    return state


def finalize_node(state: GraphState) -> GraphState:
    """Node that finalizes the conversation.
    
    Args:
        state: Current state
        
    Returns:
        State with finalization message
    """
    farewell = Message(
        performative=Performative.INFORM,
        sender="jayz-wayz",
        receiver="user",
        content={"text": "Conversation complete. Goodbye!"},
        conversation_id=state.conversation_id,
        message_id=str(uuid4())
    )
    state.add_message(farewell.to_dict())
    state.current_step = "completed"
    
    return state
