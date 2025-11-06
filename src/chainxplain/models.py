"""Data models for ChainXplain."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Contract risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ContractAnalysis(BaseModel):
    """Result of smart contract analysis."""

    address: str
    chain: str
    name: Optional[str] = None
    is_verified: bool = False
    compiler_version: Optional[str] = None
    
    # AI-generated analysis
    summary: str
    purpose: str
    risk_level: RiskLevel
    risk_factors: List[str] = Field(default_factory=list)
    key_functions: List[str] = Field(default_factory=list)
    token_info: Optional[Dict[str, Any]] = None
    
    # Technical details
    source_code: Optional[str] = None
    abi: Optional[List[Dict[str, Any]]] = None
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


class TransactionSummary(BaseModel):
    """Summary of a transaction."""

    hash: str
    from_address: str
    to_address: Optional[str] = None
    value: str
    timestamp: datetime
    method: Optional[str] = None
    status: bool = True


class WalletAnalysis(BaseModel):
    """Result of wallet analysis."""

    address: str
    chain: str
    
    # Balance info
    native_balance: str
    token_holdings: Dict[str, Any] = Field(default_factory=dict)
    
    # Transaction analysis
    total_transactions: int = 0
    recent_transactions: List[TransactionSummary] = Field(default_factory=list)
    
    # AI-generated insights
    summary: str
    activity_pattern: str
    wallet_type: str  # e.g., "DeFi user", "NFT collector", "Exchange"
    notable_interactions: List[str] = Field(default_factory=list)
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


class TransactionAnalysis(BaseModel):
    """Detailed analysis of a single transaction."""

    hash: str
    chain: str
    
    # Basic info
    from_address: str
    to_address: Optional[str] = None
    value: str
    gas_used: int
    gas_price: str
    timestamp: datetime
    status: bool
    
    # Decoded data
    method_name: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    logs: List[Dict[str, Any]] = Field(default_factory=list)
    
    # AI explanation
    explanation: str
    risks_detected: List[str] = Field(default_factory=list)
    
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


class ChainConfig(BaseModel):
    """Configuration for a blockchain."""

    name: str
    chain_id: int
    rpc_url: str
    explorer_url: str
    explorer_api_url: str
    api_key: Optional[str] = None
