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
    """Test client no longer requires Anthropic API key (supports OpenAI too)."""
    from chainxplain.config import Settings
    import os
    
    # Temporarily clear env vars
    old_openai = os.environ.get("OPENAI_API_KEY")
    old_anthropic = os.environ.get("ANTHROPIC_API_KEY")
    
    try:
        # Set test env
        os.environ["OPENAI_API_KEY"] = "test-openai-key"
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        
        # Load settings fresh
        settings = Settings()
        
        with patch("chainxplain.client.Web3Client"), \
             patch("chainxplain.client.ExplorerClient"), \
             patch("chainxplain.client.AIAnalyzer"):
            
            client = ChainExplainClient(settings=settings)
            assert client.settings.openai_api_key == "test-openai-key"
    
    finally:
        # Restore env
        if old_openai:
            os.environ["OPENAI_API_KEY"] = old_openai
        elif "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        if old_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = old_anthropic


def test_analyze_contract(mock_client, sample_contract_address):
    """Test contract analysis."""
    # Mock the analyzer response
    mock_analysis = ContractAnalysis(
        address=sample_contract_address,
        chain="ethereum",
        name="USD Coin",
        summary="Stablecoin contract",
        purpose="ERC-20 stablecoin",
        risk_level="low",
        key_functions=["transfer", "approve"],
    )
    
    mock_client.ai_analyzer = Mock()
    mock_client.ai_analyzer.analyze_contract = Mock(return_value=mock_analysis)
    mock_client.explorer_client = Mock()
    mock_client.explorer_client.get_contract_info = Mock(return_value={"is_verified": True})
    
    result = mock_client.analyze_contract(sample_contract_address, "ethereum")
    
    assert result.address == sample_contract_address
    assert result.name == "USD Coin"
    assert result.risk_level == "low"


def test_analyze_wallet(mock_client, sample_wallet_address):
    """Test wallet analysis."""
    mock_analysis = WalletAnalysis(
        address=sample_wallet_address,
        chain="ethereum",
        native_balance="10.5",
        total_transactions=1000,
        token_holdings={},
        summary="Active trading wallet",
        activity_pattern="Regular DeFi interactions",
        wallet_type="DeFi user",
    )
    
    mock_client.ai_analyzer = Mock()
    mock_client.ai_analyzer.analyze_wallet = Mock(return_value=mock_analysis)
    mock_client.web3_client = Mock()
    mock_client.web3_client.get_balance = Mock(return_value=10.5)
    mock_client.explorer_client = Mock()
    mock_client.explorer_client.get_wallet_transactions = Mock(return_value=[])
    
    result = mock_client.analyze_wallet(sample_wallet_address, "ethereum", limit=50)
    
    assert result.address == sample_wallet_address
    assert result.total_transactions == 1000


def test_analyze_transaction(mock_client, sample_tx_hash):
    """Test transaction analysis."""
    from datetime import datetime
    
    mock_analysis = TransactionAnalysis(
        hash=sample_tx_hash,
        chain="ethereum",
        status=True,
        timestamp=datetime.utcnow(),
        from_address="0xfrom",
        to_address="0xto",
        value="1.0",
        gas_used=21000,
        gas_price="20",
        explanation="Token transfer",
    )
    
    mock_client.ai_analyzer = Mock()
    mock_client.ai_analyzer.analyze_transaction = Mock(return_value=mock_analysis)
    mock_client.web3_client = Mock()
    mock_client.web3_client.get_transaction = Mock(return_value={})
    mock_client.web3_client.get_transaction_receipt = Mock(return_value={})
    
    result = mock_client.analyze_transaction(sample_tx_hash, "ethereum")
    
    assert result.hash == sample_tx_hash
    assert result.status is True


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
