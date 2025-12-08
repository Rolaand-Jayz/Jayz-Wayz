"""Jayz Wayz - LangGraph-based supervisor with checkpointing and policy enforcement.

Phase 1 Implementation for RJW-IDD:
- Async graph runner with timeout/retry behavior
- Enhanced checkpoint store with metadata, list, and rollback
- FIPA-ACL message support
- Policy Enforcement Point (PEP) with OPA and local deny fallback
- Supervisor facade integrating all components
"""

__version__ = "0.1.0"

from .state import GraphState
from .fipa import Message, Performative
from .checkpoint import CheckpointStore
from .policy import PolicyEnforcer, OPAHttpPolicyEnforcer, LocalDenyEnforcer, CompositePolicyEnforcer
from .langgraph_core import AsyncGraphRunner, RunnerConfig
from .supervisor import Supervisor
from .nodes import (
    async_node_wrapper,
    create_greeting_node,
    create_processing_node,
    create_checkpoint_node,
    validate_node,
    error_handler_node,
    finalize_node,
)

__all__ = [
    # Core
    "GraphState",
    "Message",
    "Performative",
    # Storage
    "CheckpointStore",
    # Policy
    "PolicyEnforcer",
    "OPAHttpPolicyEnforcer",
    "LocalDenyEnforcer",
    "CompositePolicyEnforcer",
    # Execution
    "AsyncGraphRunner",
    "RunnerConfig",
    "Supervisor",
    # Nodes
    "async_node_wrapper",
    "create_greeting_node",
    "create_processing_node",
    "create_checkpoint_node",
    "validate_node",
    "error_handler_node",
    "finalize_node",
]
