"""
Alchemy API client for enhanced blockchain data access.

Provides access to Alchemy's enhanced APIs including:
- Asset transfers (including NFTs and tokens)
- NFT metadata and ownership
- Token balances and metadata
- Transaction receipts with decoded logs
- Enhanced trace APIs
"""

import logging
from typing import Any, Dict, List, Optional
import httpx
from ..config import Settings

logger = logging.getLogger(__name__)


class AlchemyError(Exception):
    """Exception raised for Alchemy API errors."""
    pass


class AlchemyClient:
    """Client for Alchemy API interactions."""
    
    def __init__(self, config: Settings, chain: str = "ethereum"):
        """
        Initialize Alchemy client.
        
        Args:
            config: Application configuration
            chain: Blockchain network name
        """
        logger.info(f"Initializing Alchemy client for chain: {chain}")
        self.config = config
        self.chain = chain.lower()
        
        try:
            self.api_key = self._get_api_key()
            self.base_url = self._get_base_url()
            logger.debug(f"Alchemy client initialized: {self.base_url[:50]}...")
        except Exception as e:
            logger.error(f"Failed to initialize Alchemy client: {e}")
            raise AlchemyError(f"Alchemy initialization failed: {e}") from e
        
    def _get_api_key(self) -> Optional[str]:
        """Get the appropriate Alchemy API key for the chain."""
        chain_keys = {
            "ethereum": self.config.alchemy_ethereum_api_key,
            "polygon": self.config.alchemy_polygon_api_key,
            "arbitrum": self.config.alchemy_arbitrum_api_key,
            "base": self.config.alchemy_base_api_key,
            "optimism": self.config.alchemy_optimism_api_key,
        }
        
        # Try chain-specific key first, then fall back to default
        return chain_keys.get(self.chain) or self.config.alchemy_api_key
    
    def _get_base_url(self) -> str:
        """Get the Alchemy API base URL for the chain."""
        if not self.api_key:
            raise ValueError(f"No Alchemy API key configured for {self.chain}")
        
        network_urls = {
            "ethereum": f"https://eth-mainnet.g.alchemy.com/v2/{self.api_key}",
            "polygon": f"https://polygon-mainnet.g.alchemy.com/v2/{self.api_key}",
            "arbitrum": f"https://arb-mainnet.g.alchemy.com/v2/{self.api_key}",
            "base": f"https://base-mainnet.g.alchemy.com/v2/{self.api_key}",
            "optimism": f"https://opt-mainnet.g.alchemy.com/v2/{self.api_key}",
        }
        
        if self.chain not in network_urls:
            raise ValueError(f"Unsupported chain for Alchemy: {self.chain}")
        
        return network_urls[self.chain]
    
    async def get_asset_transfers(
        self,
        address: str,
        from_block: str = "0x0",
        to_block: str = "latest",
        category: Optional[List[str]] = None,
        max_count: int = 1000
    ) -> Dict[str, Any]:
        """
        Get asset transfers for an address (tokens, NFTs, ETH).
        
        Args:
            address: Ethereum address
            from_block: Starting block (hex or "latest")
            to_block: Ending block (hex or "latest")
            category: Transfer categories (e.g., ["external", "erc20", "erc721", "erc1155"])
            max_count: Maximum number of results
            
        Returns:
            Asset transfer data
        """
        if category is None:
            category = ["external", "erc20", "erc721", "erc1155"]
        
        params = {
            "fromBlock": from_block,
            "toBlock": to_block,
            "fromAddress": address,
            "category": category,
            "maxCount": hex(max_count),
        }
        
        return await self._make_request("alchemy_getAssetTransfers", [params])
    
    async def get_token_balances(
        self,
        address: str,
        token_type: str = "erc20"
    ) -> Dict[str, Any]:
        """
        Get token balances for an address.
        
        Args:
            address: Ethereum address
            token_type: Type of tokens ("erc20" or "DEFAULT_TOKENS")
            
        Returns:
            Token balance data
        """
        return await self._make_request(
            "alchemy_getTokenBalances",
            [address, token_type]
        )
    
    async def get_token_metadata(self, contract_address: str) -> Dict[str, Any]:
        """
        Get metadata for a token contract.
        
        Args:
            contract_address: Token contract address
            
        Returns:
            Token metadata (name, symbol, decimals, logo)
        """
        return await self._make_request(
            "alchemy_getTokenMetadata",
            [contract_address]
        )
    
    async def get_nft_metadata(
        self,
        contract_address: str,
        token_id: str,
        token_type: str = "ERC721"
    ) -> Dict[str, Any]:
        """
        Get metadata for an NFT.
        
        Args:
            contract_address: NFT contract address
            token_id: Token ID
            token_type: NFT standard ("ERC721" or "ERC1155")
            
        Returns:
            NFT metadata
        """
        return await self._make_request(
            "alchemy_getNFTMetadata",
            [contract_address, token_id, token_type]
        )
    
    async def get_nfts_for_owner(
        self,
        owner: str,
        with_metadata: bool = True,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Get all NFTs owned by an address.
        
        Args:
            owner: Owner address
            with_metadata: Include NFT metadata
            page_size: Results per page
            
        Returns:
            NFT ownership data
        """
        params = {
            "owner": owner,
            "withMetadata": with_metadata,
            "pageSize": page_size,
        }
        
        return await self._make_request("alchemy_getNFTs", [params])
    
    async def get_transaction_receipts(
        self,
        block_number: str
    ) -> Dict[str, Any]:
        """
        Get all transaction receipts for a block.
        
        Args:
            block_number: Block number (hex)
            
        Returns:
            Transaction receipts with decoded logs
        """
        return await self._make_request(
            "alchemy_getTransactionReceipts",
            [{"blockNumber": block_number}]
        )
    
    async def compute_rarity(
        self,
        contract_address: str,
        token_id: str
    ) -> Dict[str, Any]:
        """
        Compute NFT rarity score.
        
        Args:
            contract_address: NFT contract address
            token_id: Token ID
            
        Returns:
            Rarity data
        """
        return await self._make_request(
            "alchemy_computeRarity",
            [contract_address, token_id]
        )
    
    async def get_owners_for_collection(
        self,
        contract_address: str,
        with_token_balances: bool = False
    ) -> Dict[str, Any]:
        """
        Get all owners of an NFT collection.
        
        Args:
            contract_address: NFT contract address
            with_token_balances: Include token balance data
            
        Returns:
            Owner data
        """
        params = {
            "contractAddress": contract_address,
            "withTokenBalances": with_token_balances,
        }
        
        return await self._make_request(
            "alchemy_getOwnersForCollection",
            [params]
        )
    
    async def _make_request(
        self,
        method: str,
        params: List[Any]
    ) -> Dict[str, Any]:
        """
        Make a JSON-RPC request to Alchemy API.
        
        Args:
            method: RPC method name
            params: Method parameters
            
        Returns:
            Response data
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": method,
                    "params": params,
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                raise Exception(f"Alchemy API error: {data['error']}")
            
            return data.get("result", {})


def is_alchemy_available(config: Settings, chain: str = "ethereum") -> bool:
    """
    Check if Alchemy API is configured for a chain.
    
    Args:
        config: Application configuration
        chain: Chain name
        
    Returns:
        True if Alchemy API key is available
    """
    try:
        client = AlchemyClient(config, chain)
        return client.api_key is not None
    except ValueError:
        return False
