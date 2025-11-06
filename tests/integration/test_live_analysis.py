"""
Integration tests for real blockchain interactions.

These tests interact with real blockchain networks and require API keys.
"""

import pytest
from chainxplain import ChainExplainClient


@pytest.mark.integration
def test_analyze_usdc_contract(skip_if_no_keys):
    """Test analyzing USDC contract on Ethereum."""
    client = ChainExplainClient()
    
    # USDC contract address
    usdc_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    
    result = client.analyze_contract(usdc_address, "ethereum")
    
    assert result is not None
    assert result.address.lower() == usdc_address.lower()
    assert "usdc" in result.name.lower() or "usd coin" in result.name.lower()
    assert result.token_info is not None
    assert result.token_info.get("symbol") == "USDC"


@pytest.mark.integration
def test_analyze_vitalik_wallet(skip_if_no_keys):
    """Test analyzing Vitalik's wallet."""
    client = ChainExplainClient()
    
    # Vitalik's address
    vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    result = client.analyze_wallet(vitalik, "ethereum", limit=10)
    
    assert result is not None
    assert result.address.lower() == vitalik.lower()
    assert result.total_transactions > 0
    assert result.summary is not None


@pytest.mark.integration
def test_multi_chain_support(skip_if_no_keys):
    """Test analyzing contracts on different chains."""
    client = ChainExplainClient()
    
    # USDC on Polygon
    usdc_polygon = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    
    result = client.analyze_contract(usdc_polygon, "polygon")
    
    assert result is not None
    assert "usdc" in result.name.lower() or "usd coin" in result.name.lower()


@pytest.mark.integration
@pytest.mark.slow
def test_large_wallet_analysis(skip_if_no_keys):
    """Test analyzing a wallet with many transactions."""
    client = ChainExplainClient()
    
    # An active wallet
    address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    
    result = client.analyze_wallet(address, "ethereum", limit=100)
    
    assert result is not None
    assert result.total_transactions > 50  # Should have many transactions
