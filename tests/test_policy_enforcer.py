"""Tests for policy enforcers."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import aiohttp

from jayz_wayz.policy import (
    PolicyEnforcer,
    OPAHttpPolicyEnforcer,
    LocalDenyEnforcer,
    CompositePolicyEnforcer
)


@pytest.mark.asyncio
async def test_local_deny_enforcer():
    """Test that LocalDenyEnforcer denies all requests."""
    enforcer = LocalDenyEnforcer()
    
    # All actions should be denied
    assert await enforcer.enforce("read", "resource1") is False
    assert await enforcer.enforce("write", "resource2") is False
    assert await enforcer.enforce("execute", "resource3") is False
    assert await enforcer.enforce("delete", "resource4", {"user": "admin"}) is False


@pytest.mark.asyncio
async def test_opa_enforcer_allow():
    """Test OPA enforcer with allow response."""
    enforcer = OPAHttpPolicyEnforcer(opa_url="http://test-opa:8181")
    
    # Mock the session response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"result": True})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(enforcer, '_get_session') as mock_get_session:
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_response)
        mock_get_session.return_value = mock_session
        
        result = await enforcer.enforce("read", "document1")
        
        assert result is True


@pytest.mark.asyncio
async def test_opa_enforcer_deny():
    """Test OPA enforcer with deny response."""
    enforcer = OPAHttpPolicyEnforcer(opa_url="http://test-opa:8181")
    
    # Mock the session response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"result": False})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(enforcer, '_get_session') as mock_get_session:
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_response)
        mock_get_session.return_value = mock_session
        
        result = await enforcer.enforce("write", "document2")
        
        assert result is False


@pytest.mark.asyncio
async def test_opa_enforcer_non_200_response():
    """Test OPA enforcer with non-200 response (deny by default)."""
    enforcer = OPAHttpPolicyEnforcer(opa_url="http://test-opa:8181")
    
    # Mock the session response
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(enforcer, '_get_session') as mock_get_session:
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_response)
        mock_get_session.return_value = mock_session
        
        result = await enforcer.enforce("read", "document3")
        
        assert result is False


@pytest.mark.asyncio
async def test_opa_enforcer_connection_error():
    """Test OPA enforcer with connection error (raises exception)."""
    enforcer = OPAHttpPolicyEnforcer(opa_url="http://test-opa:8181")
    
    with patch.object(enforcer, '_get_session') as mock_get_session:
        mock_session = AsyncMock()
        mock_session.post = MagicMock(side_effect=aiohttp.ClientError("Connection failed"))
        mock_get_session.return_value = mock_session
        
        with pytest.raises(aiohttp.ClientError):
            await enforcer.enforce("read", "document4")


@pytest.mark.asyncio
async def test_opa_enforcer_with_context():
    """Test OPA enforcer with context data."""
    enforcer = OPAHttpPolicyEnforcer(opa_url="http://test-opa:8181")
    
    # Mock the session response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"result": True})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(enforcer, '_get_session') as mock_get_session:
        mock_session = AsyncMock()
        mock_post = MagicMock(return_value=mock_response)
        mock_session.post = mock_post
        mock_get_session.return_value = mock_session
        
        context = {"user": "alice", "role": "admin"}
        result = await enforcer.enforce("delete", "document5", context)
        
        assert result is True
        
        # Verify context was passed in the request
        call_args = mock_post.call_args
        json_data = call_args[1]["json"]
        assert json_data["input"]["context"] == context


@pytest.mark.asyncio
async def test_composite_enforcer_primary_success():
    """Test composite enforcer using primary when it succeeds."""
    primary = AsyncMock(spec=PolicyEnforcer)
    primary.enforce = AsyncMock(return_value=True)
    
    fallback = AsyncMock(spec=PolicyEnforcer)
    fallback.enforce = AsyncMock(return_value=False)
    
    composite = CompositePolicyEnforcer(primary, fallback)
    
    result = await composite.enforce("read", "resource1")
    
    assert result is True
    assert primary.enforce.called
    assert not fallback.enforce.called


@pytest.mark.asyncio
async def test_composite_enforcer_fallback_on_error():
    """Test composite enforcer falling back when primary fails."""
    primary = AsyncMock(spec=PolicyEnforcer)
    primary.enforce = AsyncMock(side_effect=Exception("Primary failed"))
    
    fallback = AsyncMock(spec=PolicyEnforcer)
    fallback.enforce = AsyncMock(return_value=False)
    
    composite = CompositePolicyEnforcer(primary, fallback)
    
    result = await composite.enforce("write", "resource2")
    
    assert result is False
    assert primary.enforce.called
    assert fallback.enforce.called


@pytest.mark.asyncio
async def test_composite_enforcer_both_deny():
    """Test composite enforcer when both deny."""
    primary = AsyncMock(spec=PolicyEnforcer)
    primary.enforce = AsyncMock(return_value=False)
    
    fallback = AsyncMock(spec=PolicyEnforcer)
    fallback.enforce = AsyncMock(return_value=False)
    
    composite = CompositePolicyEnforcer(primary, fallback)
    
    result = await composite.enforce("execute", "resource3")
    
    assert result is False
    assert primary.enforce.called
    assert not fallback.enforce.called  # Primary succeeded, no need for fallback


@pytest.mark.asyncio
async def test_opa_enforcer_session_management():
    """Test OPA enforcer session is created on demand."""
    enforcer = OPAHttpPolicyEnforcer()
    
    assert enforcer._session is None
    
    # Mock response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"result": True})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)
    
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_session.closed = False
        mock_session.post = MagicMock(return_value=mock_response)
        mock_session_class.return_value = mock_session
        
        await enforcer.enforce("read", "resource")
        
        assert mock_session_class.called


@pytest.mark.asyncio
async def test_opa_enforcer_context_manager():
    """Test OPA enforcer as context manager."""
    async with OPAHttpPolicyEnforcer() as enforcer:
        assert isinstance(enforcer, OPAHttpPolicyEnforcer)
    
    # Session should be closed after context exit
    # (actual behavior depends on implementation)


@pytest.mark.asyncio
async def test_composite_with_opa_and_local():
    """Test realistic composite with OPA primary and LocalDeny fallback."""
    primary = OPAHttpPolicyEnforcer(opa_url="http://test-opa:8181")
    fallback = LocalDenyEnforcer()
    
    composite = CompositePolicyEnforcer(primary, fallback)
    
    # Simulate OPA failure (connection error)
    with patch.object(primary, 'enforce', side_effect=aiohttp.ClientError("Connection failed")):
        result = await composite.enforce("read", "resource")
        
        # Should fall back to LocalDenyEnforcer (deny all)
        assert result is False
