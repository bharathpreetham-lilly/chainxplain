"""Blockchain explorer API client."""

import time
from typing import Any, Dict, List, Optional
from datetime import datetime

import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache

from chainxplain.config import Settings, ChainConfig


class ExplorerClient:
    """Client for blockchain explorer APIs (Etherscan, etc.)."""

    def __init__(self, settings: Settings):
        """Initialize explorer client."""
        self.settings = settings
        self._cache = TTLCache(maxsize=1000, ttl=settings.cache_ttl)
        self._rate_limiter = RateLimiter(settings.rate_limit)

    def _get_api_url(self, chain: str) -> str:
        """Get explorer API URL for a chain."""
        config = ChainConfig.get_chain_config(chain)
        return config["explorer_api"]

    def _get_api_key(self, chain: str) -> Optional[str]:
        """Get API key for a chain's explorer."""
        return ChainConfig.get_explorer_api_key(chain, self.settings)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _make_request(
        self,
        chain: str,
        module: str,
        action: str,
        **params: Any,
    ) -> Dict[str, Any]:
        """
        Make request to explorer API.

        Args:
            chain: Blockchain name
            module: API module
            action: API action
            **params: Additional parameters

        Returns:
            API response data
        """
        self._rate_limiter.wait()

        api_url = self._get_api_url(chain)
        api_key = self._get_api_key(chain)

        request_params = {
            "module": module,
            "action": action,
            **params,
        }

        if api_key:
            request_params["apikey"] = api_key

        response = requests.get(api_url, params=request_params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if data.get("status") == "0" and data.get("message") != "No transactions found":
            raise Exception(f"Explorer API error: {data.get('result', 'Unknown error')}")

        return data

    def get_contract_info(self, address: str, chain: str) -> Dict[str, Any]:
        """
        Get contract information including source code if verified.

        Args:
            address: Contract address
            chain: Blockchain name

        Returns:
            Contract information
        """
        cache_key = f"contract:{chain}:{address}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            data = self._make_request(
                chain=chain,
                module="contract",
                action="getsourcecode",
                address=address,
            )

            result = data.get("result", [{}])[0]

            contract_info = {
                "address": address,
                "is_verified": result.get("SourceCode") != "",
                "name": result.get("ContractName", "Unknown"),
                "compiler_version": result.get("CompilerVersion"),
                "optimization_used": result.get("OptimizationUsed") == "1",
                "source_code": result.get("SourceCode"),
                "abi": result.get("ABI"),
                "constructor_arguments": result.get("ConstructorArguments"),
            }

            self._cache[cache_key] = contract_info
            return contract_info

        except Exception as e:
            # Return minimal info if API fails
            return {
                "address": address,
                "is_verified": False,
                "name": "Unknown",
                "error": str(e),
            }

    def get_transactions(
        self,
        address: str,
        chain: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get normal transactions for an address.

        Args:
            address: Wallet address
            chain: Blockchain name
            limit: Number of transactions to fetch
            offset: Offset for pagination

        Returns:
            List of transactions
        """
        try:
            data = self._make_request(
                chain=chain,
                module="account",
                action="txlist",
                address=address,
                startblock=0,
                endblock=99999999,
                page=1,
                offset=limit,
                sort="desc",
            )

            transactions = []
            for tx in data.get("result", [])[:limit]:
                transactions.append({
                    "hash": tx["hash"],
                    "from": tx["from"],
                    "to": tx.get("to"),
                    "value": tx["value"],
                    "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])),
                    "block_number": int(tx["blockNumber"]),
                    "gas_used": int(tx["gasUsed"]),
                    "gas_price": tx["gasPrice"],
                    "is_error": tx.get("isError") == "1",
                    "method": tx.get("functionName", "").split("(")[0] if tx.get("functionName") else None,
                })

            return transactions

        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    def get_token_holdings(self, address: str, chain: str) -> Dict[str, Any]:
        """
        Get ERC20 token holdings for an address.

        Args:
            address: Wallet address
            chain: Blockchain name

        Returns:
            Dictionary of token holdings
        """
        try:
            data = self._make_request(
                chain=chain,
                module="account",
                action="tokentx",
                address=address,
                startblock=0,
                endblock=99999999,
                page=1,
                offset=100,
                sort="desc",
            )

            # Aggregate token transfers to calculate holdings
            tokens: Dict[str, Dict[str, Any]] = {}

            for tx in data.get("result", []):
                token_address = tx["contractAddress"]
                token_symbol = tx.get("tokenSymbol", "UNKNOWN")
                token_name = tx.get("tokenName", "Unknown Token")

                if token_address not in tokens:
                    tokens[token_address] = {
                        "symbol": token_symbol,
                        "name": token_name,
                        "address": token_address,
                    }

            return tokens

        except Exception as e:
            print(f"Error fetching token holdings: {e}")
            return {}

    def get_abi(self, address: str, chain: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get contract ABI.

        Args:
            address: Contract address
            chain: Blockchain name

        Returns:
            Contract ABI or None
        """
        contract_info = self.get_contract_info(address, chain)
        abi_str = contract_info.get("abi")

        if abi_str and abi_str != "Contract source code not verified":
            import json
            try:
                return json.loads(abi_str)
            except json.JSONDecodeError:
                return None

        return None


class RateLimiter:
    """Simple rate limiter."""

    def __init__(self, requests_per_second: int):
        """Initialize rate limiter."""
        self.min_interval = 1.0 / requests_per_second
        self.last_request = 0.0

    def wait(self) -> None:
        """Wait if necessary to respect rate limit."""
        now = time.time()
        time_since_last = now - self.last_request

        if time_since_last < self.min_interval:
            time.sleep(self.min_interval - time_since_last)

        self.last_request = time.time()
