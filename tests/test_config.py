"""Tests for configuration module."""

import pytest
from chainxplain.config import Settings, load_settings


def test_settings_from_env(monkeypatch):
    """Test loading settings from environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ETHERSCAN_API_KEY", "test-etherscan")
    
    settings = load_settings()
    
    assert settings.anthropic_api_key == "test-key"
    assert settings.etherscan_api_key == "test-etherscan"


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings(anthropic_api_key="test")
    
    assert settings.cache_ttl == 3600
    assert settings.rate_limit == 5
    assert settings.default_chain == "ethereum"


def test_get_rpc_url_default(mock_settings):
    """Test getting default RPC URL."""
    url = mock_settings.get_rpc_url("ethereum")
    assert "eth" in url.lower()


def test_get_rpc_url_with_alchemy(mock_settings):
    """Test getting Alchemy RPC URL when configured."""
    mock_settings.alchemy_api_key = "test-alchemy-key"
    url = mock_settings.get_rpc_url("ethereum")
    assert "alchemy.com" in url
    assert "test-alchemy-key" in url


def test_get_explorer_api_key(mock_settings):
    """Test getting explorer API key for chain."""
    # Ethereum uses etherscan
    key = mock_settings.get_explorer_api_key("ethereum")
    assert key == "test-etherscan-key"


def test_supported_chains(mock_settings):
    """Test that all expected chains are supported."""
    expected_chains = ["ethereum", "polygon", "arbitrum", "optimism", "base", "bsc"]
    
    for chain in expected_chains:
        url = mock_settings.get_rpc_url(chain)
        assert url is not None
        assert len(url) > 0
