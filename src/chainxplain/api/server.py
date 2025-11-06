"""FastAPI REST API server for ChainXplain."""

import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chainxplain.client import ChainExplainClient
from chainxplain.config import load_settings
from chainxplain.models import ContractAnalysis, WalletAnalysis, TransactionAnalysis
from chainxplain.validation import ValidationError
from chainxplain.logging_config import setup_logging

# Setup logging
setup_logging(level="INFO")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ChainXplain API",
    description="AI-powered blockchain analysis API for smart contracts, wallets, and transactions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize client
try:
    settings = load_settings()
    client = ChainExplainClient(settings=settings)
    logger.info("ChainXplain API server initialized")
except Exception as e:
    logger.error(f"Failed to initialize ChainXplain client: {e}")
    raise


# Request/Response Models
class ContractAnalysisRequest(BaseModel):
    """Request model for contract analysis."""
    address: str = Field(..., description="Contract address to analyze")
    chain: str = Field(default="ethereum", description="Blockchain name")
    include_source: bool = Field(default=False, description="Include source code in response")


class WalletAnalysisRequest(BaseModel):
    """Request model for wallet analysis."""
    address: str = Field(..., description="Wallet address to analyze")
    chain: str = Field(default="ethereum", description="Blockchain name")
    limit: int = Field(default=50, ge=1, le=1000, description="Number of recent transactions")


class TransactionAnalysisRequest(BaseModel):
    """Request model for transaction analysis."""
    tx_hash: str = Field(..., description="Transaction hash to analyze")
    chain: str = Field(default="ethereum", description="Blockchain name")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    ai_provider: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None


# Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with service information."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "ai_provider": client.ai_analyzer.provider,
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "ai_provider": client.ai_analyzer.provider,
    }


@app.post("/analyze/contract", response_model=ContractAnalysis, 
          responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def analyze_contract(request: ContractAnalysisRequest):
    """
    Analyze a smart contract.
    
    Provides AI-powered insights including:
    - Contract purpose and functionality
    - Risk assessment
    - Security analysis
    - Key functions
    - Token information (if applicable)
    """
    try:
        logger.info(f"Analyzing contract: {request.address} on {request.chain}")
        result = client.analyze_contract(
            address=request.address,
            chain=request.chain,
            include_source=request.include_source,
        )
        return result
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Contract analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/wallet", response_model=WalletAnalysis,
          responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def analyze_wallet(request: WalletAnalysisRequest):
    """
    Analyze a wallet's activity and holdings.
    
    Provides insights including:
    - Native token balance
    - Token holdings
    - Transaction history
    - Activity patterns
    - Wallet type classification
    """
    try:
        logger.info(f"Analyzing wallet: {request.address} on {request.chain}")
        result = client.analyze_wallet(
            address=request.address,
            chain=request.chain,
            limit=request.limit,
        )
        return result
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Wallet analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/transaction", response_model=TransactionAnalysis,
          responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def analyze_transaction(request: TransactionAnalysisRequest):
    """
    Analyze a specific transaction.
    
    Provides detailed explanation including:
    - Transaction purpose
    - Method calls and parameters
    - Token transfers
    - Security risks
    - Gas usage analysis
    """
    try:
        logger.info(f"Analyzing transaction: {request.tx_hash} on {request.chain}")
        result = client.analyze_transaction(
            tx_hash=request.tx_hash,
            chain=request.chain,
        )
        return result
    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Transaction analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# GET endpoints for simple queries
@app.get("/analyze/contract/{address}", response_model=ContractAnalysis)
async def analyze_contract_get(
    address: str,
    chain: str = Query(default="ethereum", description="Blockchain name"),
    include_source: bool = Query(default=False, description="Include source code"),
):
    """Analyze a contract (GET method for convenience)."""
    request = ContractAnalysisRequest(
        address=address,
        chain=chain,
        include_source=include_source,
    )
    return await analyze_contract(request)


@app.get("/analyze/wallet/{address}", response_model=WalletAnalysis)
async def analyze_wallet_get(
    address: str,
    chain: str = Query(default="ethereum", description="Blockchain name"),
    limit: int = Query(default=50, ge=1, le=1000, description="Transaction limit"),
):
    """Analyze a wallet (GET method for convenience)."""
    request = WalletAnalysisRequest(
        address=address,
        chain=chain,
        limit=limit,
    )
    return await analyze_wallet(request)


@app.get("/analyze/transaction/{tx_hash}", response_model=TransactionAnalysis)
async def analyze_transaction_get(
    tx_hash: str,
    chain: str = Query(default="ethereum", description="Blockchain name"),
):
    """Analyze a transaction (GET method for convenience)."""
    request = TransactionAnalysisRequest(
        tx_hash=tx_hash,
        chain=chain,
    )
    return await analyze_transaction(request)


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
