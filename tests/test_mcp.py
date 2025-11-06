"""Tests for MCP server."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from chainxplain.mcp.server import (
    analyze_contract,
    analyze_wallet,
    get_transaction_details,
    get_token_info,
    check_contract_security,
)
from chainxplain.models import ContractAnalysis, WalletAnalysis, TransactionAnalysis


@pytest.fixture
def mock_client_for_mcp():
    """Create a mock client for MCP tests."""
    client = Mock()
    
    client.analyze_contract.return_value = ContractAnalysis(
        address="0xtest",
        name="Test Contract",
        summary="Test summary",
        risk_level="low",
        key_functions=["transfer"],
        is_verified=True,
        token_info={"symbol": "TEST"},
    )
    
    client.analyze_wallet.return_value = WalletAnalysis(
        address="0xwallet",
        total_transactions=100,
        token_holdings=[],
        recent_activity=[],
        summary="Test wallet",
        insights=[],
    )
    
    client.analyze_transaction.return_value = TransactionAnalysis(
        tx_hash="0xtx",
        status="success",
        from_address="0xfrom",
        to_address="0xto",
        value="1.0",
        gas_used=21000,
        gas_price="20",
        explanation="Test tx",
    )
    
    return client


@pytest.mark.asyncio
async def test_mcp_analyze_contract(mock_client_for_mcp):
    """Test MCP analyze_contract tool."""
    with patch("chainxplain.mcp.server.get_client", return_value=mock_client_for_mcp):
        result = await analyze_contract("0xtest", "ethereum")
        
        assert result["success"] is True
        assert result["contract_address"] == "0xtest"
        assert result["name"] == "Test Contract"
        assert result["risk_level"] == "low"


@pytest.mark.asyncio
async def test_mcp_analyze_wallet(mock_client_for_mcp):
    """Test MCP analyze_wallet tool."""
    with patch("chainxplain.mcp.server.get_client", return_value=mock_client_for_mcp):
        result = await analyze_wallet("0xwallet", "ethereum", 50)
        
        assert result["success"] is True
        assert result["wallet_address"] == "0xwallet"
        assert result["total_transactions"] == 100


@pytest.mark.asyncio
async def test_mcp_get_transaction_details(mock_client_for_mcp):
    """Test MCP get_transaction_details tool."""
    with patch("chainxplain.mcp.server.get_client", return_value=mock_client_for_mcp):
        result = await get_transaction_details("0xtx", "ethereum")
        
        assert result["success"] is True
        assert result["transaction_hash"] == "0xtx"
        assert result["status"] == "success"


@pytest.mark.asyncio
async def test_mcp_get_token_info(mock_client_for_mcp):
    """Test MCP get_token_info tool."""
    with patch("chainxplain.mcp.server.get_client", return_value=mock_client_for_mcp):
        result = await get_token_info("0xtest", "ethereum")
        
        assert result["success"] is True
        assert result["token_address"] == "0xtest"


@pytest.mark.asyncio
async def test_mcp_check_contract_security(mock_client_for_mcp):
    """Test MCP check_contract_security tool."""
    with patch("chainxplain.mcp.server.get_client", return_value=mock_client_for_mcp):
        result = await check_contract_security("0xtest", "ethereum")
        
        assert result["success"] is True
        assert result["risk_level"] == "low"
        assert result["is_verified"] is True


@pytest.mark.asyncio
async def test_mcp_error_handling():
    """Test MCP error handling."""
    mock_client = Mock()
    mock_client.analyze_contract.side_effect = Exception("Test error")
    
    with patch("chainxplain.mcp.server.get_client", return_value=mock_client):
        result = await analyze_contract("0xtest", "ethereum")
        
        assert result["success"] is False
        assert "error" in result
        assert "Test error" in result["error"]
