"""
ChainXplain - AI-powered blockchain contract and wallet analyzer.
"""

# Setup logging first
from chainxplain.logging_config import setup_logging
import os

# Configure logging based on environment
log_level = os.getenv("CHAINXPLAIN_LOG_LEVEL", "INFO")
log_file = os.getenv("CHAINXPLAIN_LOG_FILE")
setup_logging(level=log_level, log_file=log_file)

from chainxplain.client import ChainExplainClient
from chainxplain.models import (
    ContractAnalysis,
    WalletAnalysis,
    TransactionAnalysis,
    ChainConfig,
)

# Convenience functions
def analyze_contract(address: str, chain: str = "ethereum") -> ContractAnalysis:
    """Quick contract analysis using environment variables."""
    client = ChainExplainClient()
    return client.analyze_contract(address, chain)


def analyze_wallet(
    address: str, chain: str = "ethereum", limit: int = 50
) -> WalletAnalysis:
    """Quick wallet analysis using environment variables."""
    client = ChainExplainClient()
    return client.analyze_wallet(address, chain, limit)


__version__ = "0.1.0"
__all__ = [
    "ChainExplainClient",
    "ContractAnalysis",
    "WalletAnalysis",
    "TransactionAnalysis",
    "ChainConfig",
    "analyze_contract",
    "analyze_wallet",
]
