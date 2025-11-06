"""Web3 client for blockchain interactions."""

import logging
from typing import Any, Dict, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
from cachetools import TTLCache
from eth_utils import is_address, to_checksum_address

from chainxplain.config import Settings, ChainConfig

logger = logging.getLogger(__name__)


class BlockchainError(Exception):
    """Raised when blockchain interaction fails."""
    pass


class Web3Client:
    """Client for Web3 blockchain interactions."""

    def __init__(self, settings: Settings):
        """Initialize Web3 client."""
        self.settings = settings
        self._connections: Dict[str, Web3] = {}
        self._cache = TTLCache(maxsize=1000, ttl=settings.cache_ttl)
        logger.info("Initialized Web3 client")

    def _get_web3(self, chain: str) -> Web3:
        """Get or create Web3 connection for a chain."""
        if chain not in self._connections:
            try:
                rpc_url = ChainConfig.get_rpc_url(chain, self.settings)
                logger.info(f"Connecting to {chain} RPC: {rpc_url[:50]}...")
                
                w3 = Web3(Web3.HTTPProvider(rpc_url))

                # Add PoA middleware for chains that need it (Polygon, BSC)
                if chain in ["polygon", "bsc"]:
                    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                    logger.debug(f"Added PoA middleware for {chain}")

                if not w3.is_connected():
                    logger.error(f"Failed to connect to {chain} RPC: {rpc_url}")
                    raise BlockchainError(f"Failed to connect to {chain} RPC: {rpc_url}")

                self._connections[chain] = w3
                logger.info(f"Successfully connected to {chain} (chain ID: {w3.eth.chain_id})")
                
            except Exception as e:
                logger.error(f"Error connecting to {chain}: {e}")
                raise BlockchainError(f"Failed to connect to {chain}: {e}") from e

        return self._connections[chain]

    def _validate_address(self, address: str) -> str:
        """Validate and checksum an Ethereum address."""
        if not is_address(address):
            logger.warning(f"Invalid address format: {address}")
            raise ValueError(f"Invalid Ethereum address: {address}")
        checksummed = to_checksum_address(address)
        logger.debug(f"Validated address: {checksummed}")
        return checksummed

    def get_balance(self, address: str, chain: str) -> str:
        """
        Get native token balance for an address.

        Args:
            address: Wallet address
            chain: Blockchain name

        Returns:
            Balance in Wei as string
            
        Raises:
            BlockchainError: If balance fetch fails
        """
        try:
            cache_key = f"balance:{chain}:{address}"
            if cache_key in self._cache:
                logger.debug(f"Cache hit for balance: {address}")
                return self._cache[cache_key]

            w3 = self._get_web3(chain)
            address = self._validate_address(address)

            logger.debug(f"Fetching balance for {address} on {chain}")
            balance = w3.eth.get_balance(address)
            balance_str = str(balance)

            self._cache[cache_key] = balance_str
            logger.info(f"Retrieved balance for {address}: {balance_str} wei")
            return balance_str
            
        except Exception as e:
            logger.error(f"Failed to get balance for {address} on {chain}: {e}")
            raise BlockchainError(f"Failed to get balance: {e}") from e

    def get_contract_code(self, address: str, chain: str) -> str:
        """
        Get contract bytecode.

        Args:
            address: Contract address
            chain: Blockchain name

        Returns:
            Bytecode as hex string
        """
        cache_key = f"code:{chain}:{address}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        w3 = self._get_web3(chain)
        address = self._validate_address(address)

        code = w3.eth.get_code(address)
        code_hex = code.hex()

        self._cache[cache_key] = code_hex
        return code_hex

    def get_transaction(self, tx_hash: str, chain: str) -> Dict[str, Any]:
        """
        Get transaction details.

        Args:
            tx_hash: Transaction hash
            chain: Blockchain name

        Returns:
            Transaction data
        """
        w3 = self._get_web3(chain)
        tx = w3.eth.get_transaction(tx_hash)

        return {
            "hash": tx["hash"].hex(),
            "from": tx["from"],
            "to": tx.get("to"),
            "value": str(tx["value"]),
            "gas": tx["gas"],
            "gas_price": str(tx.get("gasPrice", 0)),
            "nonce": tx["nonce"],
            "input": tx["input"].hex(),
            "block_number": tx.get("blockNumber"),
        }

    def get_transaction_receipt(self, tx_hash: str, chain: str) -> Dict[str, Any]:
        """
        Get transaction receipt (includes logs and status).

        Args:
            tx_hash: Transaction hash
            chain: Blockchain name

        Returns:
            Receipt data
        """
        w3 = self._get_web3(chain)
        receipt = w3.eth.get_transaction_receipt(tx_hash)

        logs = []
        for log in receipt.get("logs", []):
            logs.append({
                "address": log["address"],
                "topics": [topic.hex() for topic in log["topics"]],
                "data": log["data"].hex(),
            })

        return {
            "status": receipt.get("status", 0) == 1,
            "gas_used": receipt["gasUsed"],
            "logs": logs,
            "contract_address": receipt.get("contractAddress"),
        }

    def is_contract(self, address: str, chain: str) -> bool:
        """
        Check if an address is a contract.

        Args:
            address: Address to check
            chain: Blockchain name

        Returns:
            True if contract, False if EOA
        """
        code = self.get_contract_code(address, chain)
        return code != "0x" and len(code) > 2

    def get_block_timestamp(self, block_number: int, chain: str) -> int:
        """
        Get timestamp of a block.

        Args:
            block_number: Block number
            chain: Blockchain name

        Returns:
            Unix timestamp
        """
        w3 = self._get_web3(chain)
        block = w3.eth.get_block(block_number)
        return block["timestamp"]
