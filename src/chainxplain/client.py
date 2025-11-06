"""Main client for ChainXplain."""

import logging
from typing import Optional

from chainxplain.blockchain.web3_client import Web3Client, BlockchainError
from chainxplain.blockchain.explorer import ExplorerClient
from chainxplain.blockchain.alchemy_client import AlchemyClient, is_alchemy_available
from chainxplain.ai.analyzer import AIAnalyzer, AIAnalysisError
from chainxplain.config import Settings, ChainConfig, load_settings
from chainxplain.models import ContractAnalysis, WalletAnalysis, TransactionAnalysis
from chainxplain.validation import (
    validate_ethereum_address,
    validate_transaction_hash,
    validate_chain_name,
    validate_positive_integer,
    ValidationError,
)

logger = logging.getLogger(__name__)


class ChainExplainClient:
    """Main client for analyzing smart contracts and wallets."""

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        etherscan_api_key: Optional[str] = None,
        alchemy_api_key: Optional[str] = None,
        ethereum_rpc: Optional[str] = None,
        settings: Optional[Settings] = None,
    ):
        """
        Initialize ChainXplain client.

        Args:
            anthropic_api_key: Anthropic API key (overrides env)
            openai_api_key: OpenAI API key (overrides env)
            etherscan_api_key: Etherscan API key (overrides env)
            alchemy_api_key: Alchemy API key (overrides env) - recommended for better reliability
            ethereum_rpc: Ethereum RPC URL (overrides env)
            settings: Pre-loaded settings (for testing)
        """
        logger.info("Initializing ChainExplainClient")
        
        # Load settings
        self.settings = settings or load_settings()

        # Override with provided values
        if anthropic_api_key:
            self.settings.anthropic_api_key = anthropic_api_key
        if openai_api_key:
            self.settings.openai_api_key = openai_api_key
        if etherscan_api_key:
            self.settings.etherscan_api_key = etherscan_api_key
        if alchemy_api_key:
            self.settings.alchemy_api_key = alchemy_api_key
        if ethereum_rpc:
            self.settings.ethereum_rpc_url = ethereum_rpc

        # Validate that at least one AI API key is provided
        if not self.settings.anthropic_api_key and not self.settings.openai_api_key:
            logger.error("No AI API key provided")
            raise ValueError(
                "Either ANTHROPIC_API_KEY or OPENAI_API_KEY is required. "
                "Set one in your .env file or pass as parameter."
            )

        # Initialize components
        try:
            self.web3_client = Web3Client(self.settings)
            self.explorer_client = ExplorerClient(self.settings)
            self.ai_analyzer = AIAnalyzer(self.settings)
            logger.info("ChainExplainClient initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChainExplainClient: {e}")
            raise

    def analyze_contract(
        self,
        address: str,
        chain: str = "ethereum",
        include_source: bool = True,
    ) -> ContractAnalysis:
        """
        Analyze a smart contract.

        Args:
            address: Contract address
            chain: Blockchain name (ethereum, polygon, etc.)
            include_source: Whether to include source code in response

        Returns:
            ContractAnalysis with AI-generated insights
            
        Raises:
            ValidationError: If inputs are invalid
            BlockchainError: If blockchain interaction fails
            AIAnalysisError: If AI analysis fails
        """
        # Validate inputs
        address = validate_ethereum_address(address)
        chain = validate_chain_name(chain, list(ChainConfig.CHAINS.keys()))
        
        logger.info(f"Analyzing contract {address} on {chain}")

        # Validate chain
        ChainConfig.get_chain_config(chain)

        # Get contract info from explorer
        contract_info = self.explorer_client.get_contract_info(address, chain)

        # Get contract code if not verified
        if not contract_info.get("is_verified"):
            bytecode = self.web3_client.get_contract_code(address, chain)
            contract_info["bytecode"] = bytecode

        # Analyze with AI
        analysis = self.ai_analyzer.analyze_contract(contract_info, chain)

        if not include_source:
            analysis.source_code = None

        return analysis

    def analyze_wallet(
        self,
        address: str,
        chain: str = "ethereum",
        limit: int = 50,
    ) -> WalletAnalysis:
        """
        Analyze a wallet's activity and holdings.

        Args:
            address: Wallet address
            chain: Blockchain name
            limit: Number of recent transactions to analyze

        Returns:
            WalletAnalysis with insights
            
        Raises:
            ValidationError: If inputs are invalid
            BlockchainError: If blockchain interaction fails
            AIAnalysisError: If AI analysis fails
        """
        # Validate inputs
        address = validate_ethereum_address(address)
        chain = validate_chain_name(chain, list(ChainConfig.CHAINS.keys()))
        limit = validate_positive_integer(limit, max_value=1000, field_name="limit")
        
        logger.info(f"Analyzing wallet {address} on {chain} (limit: {limit})")
        
        # Validate chain
        ChainConfig.get_chain_config(chain)

        # Get wallet balance
        balance = self.web3_client.get_balance(address, chain)

        # Get transaction history
        transactions = self.explorer_client.get_transactions(address, chain, limit)

        # Get token holdings
        tokens = self.explorer_client.get_token_holdings(address, chain)

        # Analyze with AI
        wallet_data = {
            "address": address,
            "balance": balance,
            "transactions": transactions,
            "tokens": tokens,
        }

        analysis = self.ai_analyzer.analyze_wallet(wallet_data, chain)
        return analysis

    def analyze_transaction(
        self,
        tx_hash: str,
        chain: str = "ethereum",
    ) -> TransactionAnalysis:
        """
        Analyze a specific transaction.

        Args:
            tx_hash: Transaction hash
            chain: Blockchain name

        Returns:
            TransactionAnalysis with explanation
            
        Raises:
            ValidationError: If inputs are invalid
            BlockchainError: If blockchain interaction fails
            AIAnalysisError: If AI analysis fails
        """
        # Validate inputs
        tx_hash = validate_transaction_hash(tx_hash)
        chain = validate_chain_name(chain, list(ChainConfig.CHAINS.keys()))
        
        logger.info(f"Analyzing transaction {tx_hash} on {chain}")
        
        # Get transaction details
        tx_data = self.web3_client.get_transaction(tx_hash, chain)

        # Get transaction receipt for logs
        receipt = self.web3_client.get_transaction_receipt(tx_hash, chain)

        # Combine data
        full_tx_data = {**tx_data, "receipt": receipt}

        # Analyze with AI
        analysis = self.ai_analyzer.analyze_transaction(full_tx_data, chain)
        return analysis

    def get_contract_source(
        self,
        address: str,
        chain: str = "ethereum",
    ) -> Optional[str]:
        """
        Get verified contract source code.

        Args:
            address: Contract address
            chain: Blockchain name

        Returns:
            Source code string or None if not verified
        """
        contract_info = self.explorer_client.get_contract_info(address, chain)
        return contract_info.get("source_code")
