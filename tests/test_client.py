"""Tests for ChainXplain client."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from chainxplain.client import ChainExplainClient
from chainxplain.models import ContractAnalysis, WalletAnalysis, TransactionAnalysis


@pytest.fixture
def mock_client(mock_settings):
    """Create a ChainXplainClient with mocked dependencies."""
    with patch("chainxplain.client.Web3Client"), \
         patch("chainxplain.client.ExplorerClient"), \
         patch("chainxplain.client.AIAnalyzer"):
        
        client = ChainExplainClient(settings=mock_settings)
        return client


def test_client_initialization(mock_settings):
    """Test client initializes correctly."""
    with patch("chainxplain.client.Web3Client"), \
         patch("chainxplain.client.ExplorerClient"), \
         patch("chainxplain.client.AIAnalyzer"):
        
        client = ChainExplainClient(settings=mock_settings)
        assert client.settings == mock_settings


def test_client_requires_anthropic_key():
    """Test client requires Anthropic API key."""
    from chainxplain.config import Settings
    
    settings = Settings()  # No API key
    
    with pytest.raises(ValueError, match="Anthropic API key"):
        ChainExplainClient(settings=settings)


def test_analyze_contract(mock_client, sample_contract_address):
    """Test contract analysis."""
    # Mock the analyzer response
    mock_analysis = ContractAnalysis(
        address=sample_contract_address,
        name="USD Coin",
        summary="Stablecoin contract",
        risk_level="low",
        key_functions=["transfer", "approve"],
    )
    
    mock_client.analyzer = Mock()
    mock_client.analyzer.analyze_contract = Mock(return_value=mock_analysis)
    
    result = mock_client.analyze_contract(sample_contract_address, "ethereum")
    
    assert result.address == sample_contract_address
    assert result.name == "USD Coin"
    assert result.risk_level == "low"


def test_analyze_wallet(mock_client, sample_wallet_address):
    """Test wallet analysis."""
    mock_analysis = WalletAnalysis(
        address=sample_wallet_address,
        total_transactions=1000,
        token_holdings=[],
        recent_activity=[],
        summary="Active trading wallet",
    )
    
    mock_client.analyzer = Mock()
    mock_client.analyzer.analyze_wallet = Mock(return_value=mock_analysis)
    
    result = mock_client.analyze_wallet(sample_wallet_address, "ethereum", limit=50)
    
    assert result.address == sample_wallet_address
    assert result.total_transactions == 1000


def test_analyze_transaction(mock_client, sample_tx_hash):
    """Test transaction analysis."""
    mock_analysis = TransactionAnalysis(
        tx_hash=sample_tx_hash,
        status="success",
        from_address="0xfrom",
        to_address="0xto",
        value="1.0",
        gas_used=21000,
        gas_price="20",
        explanation="Token transfer",
    )
    
    mock_client.analyzer = Mock()
    mock_client.analyzer.analyze_transaction = Mock(return_value=mock_analysis)
    
    result = mock_client.analyze_transaction(sample_tx_hash, "ethereum")
    
    assert result.tx_hash == sample_tx_hash
    assert result.status == "success"


def test_client_with_custom_api_keys():
    """Test client with custom API keys."""
    with patch("chainxplain.client.Web3Client"), \
         patch("chainxplain.client.ExplorerClient"), \
         patch("chainxplain.client.AIAnalyzer"):
        
        client = ChainExplainClient(
            anthropic_api_key="custom-anthropic",
            etherscan_api_key="custom-etherscan",
            alchemy_api_key="custom-alchemy",
        )
        
        assert client.settings.anthropic_api_key == "custom-anthropic"
        assert client.settings.etherscan_api_key == "custom-etherscan"
        assert client.settings.alchemy_api_key == "custom-alchemy"
