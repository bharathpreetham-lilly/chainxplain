"""Tests for CLI interface."""

import pytest
from typer.testing import CliRunner
from chainxplain.cli.main import app
from unittest.mock import patch, Mock
from chainxplain.models import ContractAnalysis, WalletAnalysis, TransactionAnalysis


runner = CliRunner()


@pytest.fixture
def mock_client_instance():
    """Create a mock client instance."""
    client = Mock()
    
    # Mock contract analysis
    client.analyze_contract.return_value = ContractAnalysis(
        address="0xtest",
        chain="ethereum",
        name="Test Token",
        summary="A test token contract",
        purpose="ERC-20 token for testing",
        risk_level="low",
        key_functions=["transfer", "approve"],
        is_verified=True,
        token_info={"symbol": "TEST", "decimals": 18},
    )
    
    # Mock wallet analysis
    client.analyze_wallet.return_value = WalletAnalysis(
        address="0xwallet",
        chain="ethereum",
        native_balance="10.5",
        total_transactions=100,
        token_holdings={"ETH": {"balance": 10.5, "value_usd": 21000}},
        summary="Active wallet",
        activity_pattern="Regular DeFi interactions",
        wallet_type="DeFi user",
        notable_interactions=["Frequently trades tokens"],
    )
    
    # Mock transaction analysis
    from datetime import datetime
    client.analyze_transaction.return_value = TransactionAnalysis(
        hash="0xtx",
        chain="ethereum",
        status=True,
        timestamp=datetime.utcnow(),
        from_address="0xfrom",
        to_address="0xto",
        value="1.0",
        gas_used=21000,
        gas_price="20",
        explanation="Simple ETH transfer",
    )
    
    return client


def test_cli_explain_command(mock_client_instance):
    """Test explain command."""
    with patch("chainxplain.cli.main.get_client", return_value=mock_client_instance):
        result = runner.invoke(app, ["explain", "0xtest", "--chain", "ethereum"])
        
        assert result.exit_code == 0
        assert "Test Token" in result.stdout
        assert "low" in result.stdout.lower()


def test_cli_wallet_command(mock_client_instance):
    """Test wallet command."""
    with patch("chainxplain.cli.main.get_client", return_value=mock_client_instance):
        result = runner.invoke(app, ["wallet", "0xwallet", "--limit", "50"])
        
        assert result.exit_code == 0
        assert "Active wallet" in result.stdout


def test_cli_tx_command(mock_client_instance):
    """Test tx command."""
    with patch("chainxplain.cli.main.get_client", return_value=mock_client_instance):
        result = runner.invoke(app, ["tx", "0xtx", "--chain", "ethereum"])
        
        assert result.exit_code == 0
        assert "success" in result.stdout.lower()


def test_cli_token_command(mock_client_instance):
    """Test token command."""
    with patch("chainxplain.cli.main.get_client", return_value=mock_client_instance):
        result = runner.invoke(app, ["token", "0xtest"])
        
        assert result.exit_code == 0
        assert "Test Token" in result.stdout


def test_cli_version_command():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    
    assert result.exit_code == 0
    assert "ChainXplain" in result.stdout
    assert "0.1.0" in result.stdout


def test_cli_help_command():
    """Test help command."""
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "ChainXplain" in result.stdout or "blockchain" in result.stdout


def test_cli_explain_verbose(mock_client_instance):
    """Test explain command with verbose flag."""
    with patch("chainxplain.cli.main.get_client", return_value=mock_client_instance):
        result = runner.invoke(app, ["explain", "0xtest", "--verbose"])
        
        if result.exit_code != 0:
            print(f"Error output: {result.stdout}")
            print(f"Exception: {result.exception}")
        
        assert result.exit_code == 0
