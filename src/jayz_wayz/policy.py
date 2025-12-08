"""Policy Enforcement Point (PEP) with OPA HTTP enforcer and local deny fallback."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import aiohttp


class PolicyEnforcer(ABC):
    """Abstract base class for policy enforcement."""
    
    @abstractmethod
    async def enforce(
        self,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if an action on a resource is allowed.
        
        Args:
            action: The action being attempted (e.g., 'read', 'write', 'execute')
            resource: The resource being accessed
            context: Additional context for policy decision
            
        Returns:
            True if action is allowed, False otherwise
        """
        pass


class OPAHttpPolicyEnforcer(PolicyEnforcer):
    """Policy enforcer using Open Policy Agent (OPA) HTTP API.
    
    Attributes:
        opa_url: URL of the OPA server (e.g., 'http://localhost:8181')
        policy_path: Path to the policy (e.g., 'v1/data/authz/allow')
        timeout: Request timeout in seconds
        session: Aiohttp client session
    """
    
    def __init__(
        self,
        opa_url: str = "http://localhost:8181",
        policy_path: str = "v1/data/authz/allow",
        timeout: int = 5
    ):
        """Initialize OPA HTTP enforcer.
        
        Args:
            opa_url: OPA server URL
            policy_path: Path to the policy decision endpoint
            timeout: Request timeout in seconds
        """
        self.opa_url = opa_url.rstrip("/")
        self.policy_path = policy_path.lstrip("/")
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def enforce(
        self,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if action is allowed via OPA HTTP API.
        
        Args:
            action: The action being attempted
            resource: The resource being accessed
            context: Additional context for policy decision
            
        Returns:
            True if allowed, False otherwise
            
        Raises:
            aiohttp.ClientError: If OPA server is unreachable
        """
        context = context or {}
        
        # Build OPA input
        input_data = {
            "input": {
                "action": action,
                "resource": resource,
                "context": context
            }
        }
        
        session = await self._get_session()
        url = f"{self.opa_url}/{self.policy_path}"
        
        try:
            async with session.post(
                url,
                json=input_data,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # OPA returns {"result": true/false}
                    return result.get("result", False)
                else:
                    # If OPA returns non-200, deny by default
                    return False
        except (aiohttp.ClientError, asyncio.TimeoutError):
            # If OPA is unreachable, deny by default (fail-closed)
            raise
    
    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self) -> "OPAHttpPolicyEnforcer":
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()


class LocalDenyEnforcer(PolicyEnforcer):
    """Conservative local policy enforcer that denies all actions by default.
    
    This is a fallback enforcer used when the primary policy service is unavailable.
    It implements a fail-closed security policy.
    """
    
    async def enforce(
        self,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Deny all actions by default (fail-closed).
        
        Args:
            action: The action being attempted
            resource: The resource being accessed
            context: Additional context (ignored)
            
        Returns:
            Always returns False (deny)
        """
        return False


class CompositePolicyEnforcer(PolicyEnforcer):
    """Policy enforcer that tries primary enforcer, falls back to secondary.
    
    Attributes:
        primary: Primary policy enforcer (e.g., OPA)
        fallback: Fallback enforcer (e.g., LocalDenyEnforcer)
    """
    
    def __init__(self, primary: PolicyEnforcer, fallback: PolicyEnforcer):
        """Initialize composite enforcer.
        
        Args:
            primary: Primary policy enforcer
            fallback: Fallback enforcer
        """
        self.primary = primary
        self.fallback = fallback
    
    async def enforce(
        self,
        action: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Try primary enforcer, fall back on error.
        
        Args:
            action: The action being attempted
            resource: The resource being accessed
            context: Additional context for policy decision
            
        Returns:
            Policy decision from primary or fallback
        """
        try:
            return await self.primary.enforce(action, resource, context)
        except Exception:
            # If primary fails, use fallback
            return await self.fallback.enforce(action, resource, context)
