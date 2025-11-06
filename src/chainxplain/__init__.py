"""
ChainXplain - AI-powered blockchain contract and wallet analyzer.
"""

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
