"""
FastMCP server for ChainXplain.

Exposes blockchain analysis tools to AI agents like Claude Desktop.
"""

from typing import Any, Dict, Optional
import asyncio
from fastmcp import FastMCP

from chainxplain.client import ChainExplainClient
from chainxplain.config import load_settings


# Create FastMCP server
mcp = FastMCP("ChainXplain")


# Initialize client (will be set on server start)
_client: Optional[ChainExplainClient] = None


def get_client() -> ChainExplainClient:
    """Get or create the ChainXplain client."""
    global _client
    if _client is None:
        settings = load_settings()
        _client = ChainExplainClient(settings=settings)
    return _client


@mcp.tool()
async def analyze_contract(
    address: str,
    chain: str = "ethereum"
) -> Dict[str, Any]:
    """
    Analyze a smart contract and explain what it does.
    
    This tool provides AI-powered analysis of smart contracts including:
    - Contract purpose and functionality
    - Security risk assessment
    - Key functions and their purposes
    - Token information (if applicable)
    
    Args:
        address: Contract address (0x-prefixed hex string)
        chain: Blockchain network (ethereum, polygon, arbitrum, base, optimism, bsc)
        
    Returns:
        Analysis results including summary, risk level, and details
        
    Example:
        analyze_contract("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "ethereum")
    """
    client = get_client()
    
    try:
        result = await asyncio.to_thread(
            client.analyze_contract,
            address=address,
            chain=chain
        )
        
        return {
            "success": True,
            "contract_address": address,
            "chain": chain,
            "name": result.name,
            "summary": result.summary,
            "risk_level": result.risk_level,
            "key_functions": result.key_functions,
            "token_info": result.token_info,
            "analysis": result.detailed_analysis,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "contract_address": address,
            "chain": chain,
        }


@mcp.tool()
async def analyze_wallet(
    address: str,
    chain: str = "ethereum",
    limit: int = 50
) -> Dict[str, Any]:
    """
    Analyze a wallet's activity and transaction history.
    
    This tool provides comprehensive wallet analysis including:
    - Recent transaction patterns
    - Token holdings and balances
    - DeFi protocol interactions
    - Activity summary and insights
    
    Args:
        address: Wallet address (0x-prefixed hex string)
        chain: Blockchain network (ethereum, polygon, arbitrum, base, optimism, bsc)
        limit: Maximum number of recent transactions to analyze (default: 50)
        
    Returns:
        Wallet analysis including transactions, holdings, and activity summary
        
    Example:
        analyze_wallet("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "ethereum", 50)
    """
    client = get_client()
    
    try:
        result = await asyncio.to_thread(
            client.analyze_wallet,
            address=address,
            chain=chain,
            limit=limit
        )
        
        return {
            "success": True,
            "wallet_address": address,
            "chain": chain,
            "total_transactions": result.total_transactions,
            "token_holdings": result.token_holdings,
            "recent_activity": result.recent_activity,
            "summary": result.summary,
            "insights": result.insights,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "wallet_address": address,
            "chain": chain,
        }


@mcp.tool()
async def get_transaction_details(
    tx_hash: str,
    chain: str = "ethereum"
) -> Dict[str, Any]:
    """
    Get detailed information about a specific transaction.
    
    Provides human-readable explanation of what happened in a transaction:
    - Transaction status and basic info
    - Value transferred
    - Gas used and fees
    - Contract interactions
    - Events emitted
    
    Args:
        tx_hash: Transaction hash (0x-prefixed hex string)
        chain: Blockchain network (ethereum, polygon, arbitrum, base, optimism, bsc)
        
    Returns:
        Transaction details and AI-powered explanation
        
    Example:
        get_transaction_details("0xabc123...", "ethereum")
    """
    client = get_client()
    
    try:
        result = await asyncio.to_thread(
            client.analyze_transaction,
            tx_hash=tx_hash,
            chain=chain
        )
        
        return {
            "success": True,
            "transaction_hash": tx_hash,
            "chain": chain,
            "status": result.status,
            "from_address": result.from_address,
            "to_address": result.to_address,
            "value": result.value,
            "gas_used": result.gas_used,
            "gas_price": result.gas_price,
            "explanation": result.explanation,
            "contract_calls": result.contract_calls,
            "events": result.events,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "transaction_hash": tx_hash,
            "chain": chain,
        }


@mcp.tool()
async def get_token_info(
    token_address: str,
    chain: str = "ethereum"
) -> Dict[str, Any]:
    """
    Get detailed information about a token (ERC20, ERC721, ERC1155).
    
    Provides comprehensive token information:
    - Token name, symbol, and decimals
    - Total supply
    - Contract verification status
    - Holder count (if available)
    - Token type (ERC20, ERC721, etc.)
    
    Args:
        token_address: Token contract address (0x-prefixed hex string)
        chain: Blockchain network (ethereum, polygon, arbitrum, base, optimism, bsc)
        
    Returns:
        Token information and metadata
        
    Example:
        get_token_info("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "ethereum")
    """
    client = get_client()
    
    try:
        # Use the contract analysis for token info
        result = await asyncio.to_thread(
            client.analyze_contract,
            address=token_address,
            chain=chain
        )
        
        return {
            "success": True,
            "token_address": token_address,
            "chain": chain,
            "name": result.token_info.get("name") if result.token_info else None,
            "symbol": result.token_info.get("symbol") if result.token_info else None,
            "decimals": result.token_info.get("decimals") if result.token_info else None,
            "total_supply": result.token_info.get("total_supply") if result.token_info else None,
            "token_type": result.token_info.get("type") if result.token_info else None,
            "summary": result.summary,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "token_address": token_address,
            "chain": chain,
        }


@mcp.tool()
async def check_contract_security(
    address: str,
    chain: str = "ethereum"
) -> Dict[str, Any]:
    """
    Perform security analysis on a smart contract.
    
    Analyzes contract for common security issues and risks:
    - Contract verification status
    - Known vulnerabilities
    - Risk assessment
    - Security recommendations
    
    Args:
        address: Contract address (0x-prefixed hex string)
        chain: Blockchain network (ethereum, polygon, arbitrum, base, optimism, bsc)
        
    Returns:
        Security analysis and risk assessment
        
    Example:
        check_contract_security("0x123...", "ethereum")
    """
    client = get_client()
    
    try:
        result = await asyncio.to_thread(
            client.analyze_contract,
            address=address,
            chain=chain
        )
        
        return {
            "success": True,
            "contract_address": address,
            "chain": chain,
            "risk_level": result.risk_level,
            "is_verified": result.is_verified,
            "security_issues": result.security_issues,
            "recommendations": result.recommendations,
            "summary": result.summary,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "contract_address": address,
            "chain": chain,
        }


@mcp.resource("config://supported-chains")
async def get_supported_chains() -> str:
    """
    Get list of supported blockchain networks.
    
    Returns a list of all blockchain networks supported by ChainXplain.
    """
    chains = [
        "ethereum - Ethereum Mainnet",
        "polygon - Polygon (Matic) Mainnet",
        "arbitrum - Arbitrum One",
        "optimism - Optimism Mainnet",
        "base - Base Mainnet",
        "bsc - Binance Smart Chain",
    ]
    return "\n".join(chains)


@mcp.resource("config://api-status")
async def get_api_status() -> str:
    """
    Check the status of configured API providers.
    
    Returns information about which API providers are configured and available.
    """
    settings = load_settings()
    
    status = []
    status.append("API Provider Status:")
    status.append(f"✅ Anthropic API: {'Configured' if settings.anthropic_api_key else '❌ Not configured'}")
    status.append(f"{'✅' if settings.etherscan_api_key else '⚠️'} Etherscan API: {'Configured' if settings.etherscan_api_key else 'Not configured'}")
    status.append(f"{'✅' if settings.alchemy_api_key else '⚠️'} Alchemy API: {'Configured' if settings.alchemy_api_key else 'Not configured (optional)'}")
    
    return "\n".join(status)


def create_server() -> FastMCP:
    """Create and return the FastMCP server instance."""
    return mcp


def main():
    """Run the MCP server."""
    import sys
    
    # Check if API keys are configured
    try:
        settings = load_settings()
        if not settings.anthropic_api_key:
            print("❌ Error: ANTHROPIC_API_KEY not configured", file=sys.stderr)
            print("Please set your Anthropic API key in .env or environment variables", file=sys.stderr)
            sys.exit(1)
        
        print("🚀 Starting ChainXplain MCP Server...")
        print(f"✅ Anthropic API: Configured")
        print(f"{'✅' if settings.etherscan_api_key else '⚠️'} Etherscan API: {'Configured' if settings.etherscan_api_key else 'Not configured'}")
        print(f"{'✅' if settings.alchemy_api_key else '⚠️'} Alchemy API: {'Configured' if settings.alchemy_api_key else 'Not configured (optional)'}")
        print("\n📡 Server ready to accept connections...")
        
        # Run the server
        mcp.run()
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
