"""Configuration management for ChainXplain."""

import os
from pathlib import Path
from typing import Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ChainXplain settings loaded from environment variables or .env file."""

    # AI API Keys
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")

    # Blockchain Explorer API keys
    etherscan_api_key: Optional[str] = None
    polygonscan_api_key: Optional[str] = None
    arbiscan_api_key: Optional[str] = None
    bscscan_api_key: Optional[str] = None
    optimistic_etherscan_api_key: Optional[str] = None
    basescan_api_key: Optional[str] = None
    
    # Alchemy API keys (preferred for reliability)
    alchemy_api_key: Optional[str] = None  # Default key for all chains
    alchemy_ethereum_api_key: Optional[str] = None
    alchemy_polygon_api_key: Optional[str] = None
    alchemy_arbitrum_api_key: Optional[str] = None
    alchemy_base_api_key: Optional[str] = None
    alchemy_optimism_api_key: Optional[str] = None

    # RPC Endpoints (optional, defaults to public RPCs)
    ethereum_rpc_url: str = Field(
        default="https://eth.llamarpc.com", alias="ETHEREUM_RPC_URL"
    )
    polygon_rpc_url: str = Field(
        default="https://polygon.llamarpc.com", alias="POLYGON_RPC_URL"
    )
    arbitrum_rpc_url: str = Field(
        default="https://arb1.arbitrum.io/rpc", alias="ARBITRUM_RPC_URL"
    )
    optimism_rpc_url: str = Field(
        default="https://mainnet.optimism.io", alias="OPTIMISM_RPC_URL"
    )
    bsc_rpc_url: str = Field(
        default="https://bsc-dataseed.binance.org", alias="BSC_RPC_URL"
    )

    # Advanced Settings
    cache_ttl: int = Field(default=3600, alias="CACHE_TTL")
    rate_limit: int = Field(default=5, alias="RATE_LIMIT")
    default_chain: str = Field(default="ethereum", alias="DEFAULT_CHAIN")
    claude_model: str = Field(
        default="claude-3-5-sonnet-20241022", alias="CLAUDE_MODEL"
    )
    max_tokens: int = Field(default=4096, alias="MAX_TOKENS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class ChainConfig:
    """Chain-specific configuration."""

    CHAINS: Dict[str, dict] = {
        "ethereum": {
            "name": "Ethereum",
            "chain_id": 1,
            "explorer": "https://etherscan.io",
            "explorer_api": "https://api.etherscan.io/api",
            "rpc_key": "ethereum_rpc_url",
            "api_key": "etherscan_api_key",
        },
        "polygon": {
            "name": "Polygon",
            "chain_id": 137,
            "explorer": "https://polygonscan.com",
            "explorer_api": "https://api.polygonscan.com/api",
            "rpc_key": "polygon_rpc_url",
            "api_key": "polygonscan_api_key",
        },
        "arbitrum": {
            "name": "Arbitrum One",
            "chain_id": 42161,
            "explorer": "https://arbiscan.io",
            "explorer_api": "https://api.arbiscan.io/api",
            "rpc_key": "arbitrum_rpc_url",
            "api_key": "arbiscan_api_key",
        },
        "optimism": {
            "name": "Optimism",
            "chain_id": 10,
            "explorer": "https://optimistic.etherscan.io",
            "explorer_api": "https://api-optimistic.etherscan.io/api",
            "rpc_key": "optimism_rpc_url",
            "api_key": "optimistic_etherscan_api_key",
        },
        "bsc": {
            "name": "BNB Smart Chain",
            "chain_id": 56,
            "explorer": "https://bscscan.com",
            "explorer_api": "https://api.bscscan.com/api",
            "rpc_key": "bsc_rpc_url",
            "api_key": "bscscan_api_key",
        },
    }

    @classmethod
    def get_chain_config(cls, chain: str) -> dict:
        """Get configuration for a specific chain."""
        if chain not in cls.CHAINS:
            raise ValueError(
                f"Unsupported chain: {chain}. "
                f"Supported chains: {', '.join(cls.CHAINS.keys())}"
            )
        return cls.CHAINS[chain]

    def get_rpc_url(self, chain: str) -> str:
        """Get RPC URL for a specific chain, using Alchemy if available."""
        chain = chain.lower()
        
        # Check for chain-specific Alchemy key first
        alchemy_key = None
        if chain == "ethereum" and self.alchemy_ethereum_api_key:
            alchemy_key = self.alchemy_ethereum_api_key
        elif chain == "polygon" and self.alchemy_polygon_api_key:
            alchemy_key = self.alchemy_polygon_api_key
        elif chain == "arbitrum" and self.alchemy_arbitrum_api_key:
            alchemy_key = self.alchemy_arbitrum_api_key
        elif chain == "base" and self.alchemy_base_api_key:
            alchemy_key = self.alchemy_base_api_key
        elif chain == "optimism" and self.alchemy_optimism_api_key:
            alchemy_key = self.alchemy_optimism_api_key
        elif self.alchemy_api_key:
            alchemy_key = self.alchemy_api_key
        
        # If Alchemy key is available, use Alchemy RPC
        if alchemy_key:
            alchemy_networks = {
                "ethereum": f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_key}",
                "polygon": f"https://polygon-mainnet.g.alchemy.com/v2/{alchemy_key}",
                "arbitrum": f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_key}",
                "base": f"https://base-mainnet.g.alchemy.com/v2/{alchemy_key}",
                "optimism": f"https://opt-mainnet.g.alchemy.com/v2/{alchemy_key}",
            }
            if chain in alchemy_networks:
                return alchemy_networks[chain]
        
        # Fallback to custom RPC or public RPCs
        custom_rpc = self.rpc_urls.get(chain)
        if custom_rpc:
            return custom_rpc
        
        return self._default_rpc_urls.get(chain, "https://eth.llamarpc.com")

    @classmethod
    def get_explorer_api_key(cls, chain: str, settings: Settings) -> Optional[str]:
        """Get explorer API key for a chain."""
        config = cls.get_chain_config(chain)
        api_key_field = config["api_key"]
        return getattr(settings, api_key_field, None)


def load_settings() -> Settings:
    """Load settings from environment or .env file."""
    return Settings()
