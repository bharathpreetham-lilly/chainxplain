"""Test configuration and fixtures."""

import pytest
from unittest.mock import Mock
from chainxplain.config import Settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    return Settings(
        anthropic_api_key="test-anthropic-key",
        etherscan_api_key="test-etherscan-key",
        alchemy_api_key="test-alchemy-key",
        ethereum_rpc_url="https://test-rpc.com",
    )


@pytest.fixture
def sample_contract_address():
    """Sample contract address for testing."""
    return "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC


@pytest.fixture
def sample_wallet_address():
    """Sample wallet address for testing."""
    return "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"


@pytest.fixture
def sample_tx_hash():
    """Sample transaction hash for testing."""
    return "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
