"""Tests for data models."""

import pytest
from chainxplain.models import (
    ContractAnalysis,
    WalletAnalysis,
    TransactionAnalysis,
    ChainConfig,
)


def test_contract_analysis_creation():
    """Test creating ContractAnalysis model."""
    analysis = ContractAnalysis(
        address="0xtest",
        name="Test Contract",
        summary="A test contract",
        risk_level="low",
        key_functions=["transfer", "approve"],
    )
    
    assert analysis.address == "0xtest"
    assert analysis.name == "Test Contract"
    assert analysis.risk_level == "low"
    assert len(analysis.key_functions) == 2


def test_wallet_analysis_creation():
    """Test creating WalletAnalysis model."""
    analysis = WalletAnalysis(
        address="0xwallet",
        total_transactions=100,
        token_holdings=[],
        recent_activity=[],
        summary="Active wallet",
    )
    
    assert analysis.address == "0xwallet"
    assert analysis.total_transactions == 100
    assert analysis.summary == "Active wallet"


def test_transaction_analysis_creation():
    """Test creating TransactionAnalysis model."""
    analysis = TransactionAnalysis(
        tx_hash="0xtx",
        status="success",
        from_address="0xfrom",
        to_address="0xto",
        value="1.0",
        gas_used=21000,
        gas_price="20",
        explanation="Simple transfer",
    )
    
    assert analysis.tx_hash == "0xtx"
    assert analysis.status == "success"
    assert analysis.gas_used == 21000


def test_chain_config_creation():
    """Test creating ChainConfig model."""
    config = ChainConfig(
        name="ethereum",
        rpc_url="https://eth.llamarpc.com",
        explorer_url="https://etherscan.io",
        chain_id=1,
    )
    
    assert config.name == "ethereum"
    assert config.chain_id == 1
    assert "etherscan" in config.explorer_url


def test_contract_analysis_validation():
    """Test ContractAnalysis validation."""
    # Risk level should be validated
    with pytest.raises(Exception):  # Pydantic validation error
        ContractAnalysis(
            address="0xtest",
            summary="test",
            risk_level="invalid",  # Invalid risk level
        )
