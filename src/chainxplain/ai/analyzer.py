"""AI-powered analysis using Claude or OpenAI."""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from chainxplain.config import Settings
from chainxplain.models import (
    ContractAnalysis,
    WalletAnalysis,
    TransactionAnalysis,
    RiskLevel,
    TransactionSummary,
)

logger = logging.getLogger(__name__)


class AIAnalysisError(Exception):
    """Raised when AI analysis fails."""
    pass


class AIAnalyzer:
    """AI analyzer using Claude or OpenAI for smart contract and wallet analysis."""

    def __init__(self, settings: Settings):
        """Initialize AI analyzer."""
        self.settings = settings
        self.max_tokens = settings.max_tokens
        
        # Determine which AI provider to use
        try:
            if settings.openai_api_key:
                from openai import OpenAI
                self.provider = "openai"
                self.client = OpenAI(api_key=settings.openai_api_key)
                self.model = "gpt-4o"  # Latest GPT-4 model
                logger.info(f"Initialized AI analyzer with OpenAI (model: {self.model})")
            elif settings.anthropic_api_key:
                from anthropic import Anthropic
                self.provider = "anthropic"
                self.client = Anthropic(api_key=settings.anthropic_api_key)
                self.model = settings.claude_model
                logger.info(f"Initialized AI analyzer with Anthropic (model: {self.model})")
            else:
                raise ValueError(
                    "Either OPENAI_API_KEY or ANTHROPIC_API_KEY must be set. "
                    "Set one in your .env file."
                )
        except ImportError as e:
            logger.error(f"Failed to import AI provider library: {e}")
            raise AIAnalysisError(f"AI provider library not installed: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize AI analyzer: {e}")
            raise

    def analyze_contract(
        self,
        contract_info: Dict[str, Any],
        chain: str,
    ) -> ContractAnalysis:
        """
        Analyze a smart contract using AI (Claude or OpenAI).

        Args:
            contract_info: Contract information from explorer
            chain: Blockchain name

        Returns:
            ContractAnalysis with AI-generated insights
            
        Raises:
            AIAnalysisError: If analysis fails
        """
        try:
            logger.info(f"Analyzing contract {contract_info.get('address')} on {chain}")
            
            # Build analysis prompt
            prompt = self._build_contract_prompt(contract_info, chain)

            # Call AI provider
            analysis_text = self._call_ai(prompt)
            
            logger.debug(f"Received AI response: {len(analysis_text)} characters")

            # Extract structured data from response
            analysis_data = self._parse_contract_analysis(analysis_text)

            # Build ContractAnalysis object
            result = ContractAnalysis(
                address=contract_info["address"],
                chain=chain,
                name=contract_info.get("name", "Unknown"),
                is_verified=contract_info.get("is_verified", False),
                compiler_version=contract_info.get("compiler_version"),
                summary=analysis_data.get("summary", analysis_text[:500]),
                purpose=analysis_data.get("purpose", "Unknown"),
                risk_level=RiskLevel(analysis_data.get("risk_level", "unknown")),
                risk_factors=analysis_data.get("risk_factors", []),
                key_functions=analysis_data.get("key_functions", []),
                token_info=analysis_data.get("token_info"),
                source_code=contract_info.get("source_code"),
                abi=contract_info.get("abi"),
            )
            
            logger.info(f"Successfully analyzed contract: {result.name} (risk: {result.risk_level})")
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze contract {contract_info.get('address')}: {e}")
            raise AIAnalysisError(f"Contract analysis failed: {e}") from e

    def analyze_wallet(
        self,
        wallet_data: Dict[str, Any],
        chain: str,
    ) -> WalletAnalysis:
        """
        Analyze a wallet using AI (Claude or OpenAI).

        Args:
            wallet_data: Wallet data (balance, transactions, tokens)
            chain: Blockchain name

        Returns:
            WalletAnalysis with insights
        """
        # Build analysis prompt
        prompt = self._build_wallet_prompt(wallet_data, chain)

        # Call AI provider
        analysis_text = self._call_ai(prompt)
        analysis_data = self._parse_wallet_analysis(analysis_text)

        # Convert transactions to TransactionSummary
        recent_txs = []
        for tx in wallet_data.get("transactions", [])[:10]:
            recent_txs.append(
                TransactionSummary(
                    hash=tx["hash"],
                    from_address=tx["from"],
                    to_address=tx.get("to"),
                    value=tx["value"],
                    timestamp=tx["timestamp"],
                    method=tx.get("method"),
                    status=not tx.get("is_error", False),
                )
            )

        return WalletAnalysis(
            address=wallet_data["address"],
            chain=chain,
            native_balance=wallet_data.get("balance", "0"),
            token_holdings=wallet_data.get("tokens", {}),
            total_transactions=len(wallet_data.get("transactions", [])),
            recent_transactions=recent_txs,
            summary=analysis_data.get("summary", analysis_text[:500]),
            activity_pattern=analysis_data.get("activity_pattern", "Unknown"),
            wallet_type=analysis_data.get("wallet_type", "Unknown"),
            notable_interactions=analysis_data.get("notable_interactions", []),
        )

    def analyze_transaction(
        self,
        tx_data: Dict[str, Any],
        chain: str,
    ) -> TransactionAnalysis:
        """
        Analyze a transaction using AI (Claude or OpenAI).

        Args:
            tx_data: Transaction data
            chain: Blockchain name

        Returns:
            TransactionAnalysis with explanation
        """
        prompt = self._build_transaction_prompt(tx_data, chain)

        # Call AI provider
        analysis_text = self._call_ai(prompt)
        analysis_data = self._parse_transaction_analysis(analysis_text)

        return TransactionAnalysis(
            hash=tx_data["hash"],
            chain=chain,
            from_address=tx_data["from"],
            to_address=tx_data.get("to"),
            value=tx_data["value"],
            gas_used=tx_data.get("receipt", {}).get("gas_used", 0),
            gas_price=tx_data.get("gas_price", "0"),
            timestamp=datetime.now(),  # Should be fetched from block
            status=tx_data.get("receipt", {}).get("status", True),
            method_name=analysis_data.get("method_name"),
            parameters=analysis_data.get("parameters"),
            logs=tx_data.get("receipt", {}).get("logs", []),
            explanation=analysis_data.get("explanation", analysis_text),
            risks_detected=analysis_data.get("risks", []),
        )

    def _build_contract_prompt(self, contract_info: Dict[str, Any], chain: str) -> str:
        """Build prompt for contract analysis."""
        prompt = f"""Analyze this smart contract on {chain}:

Address: {contract_info['address']}
Name: {contract_info.get('name', 'Unknown')}
Verified: {contract_info.get('is_verified', False)}

"""

        if contract_info.get("source_code"):
            source = contract_info["source_code"]
            # Truncate if too long
            if len(source) > 10000:
                source = source[:10000] + "\n... (truncated)"
            prompt += f"Source Code:\n```solidity\n{source}\n```\n\n"
        elif contract_info.get("abi"):
            prompt += f"ABI:\n```json\n{contract_info['abi']}\n```\n\n"
        else:
            prompt += "Source code not available (unverified contract)\n\n"

        prompt += """Please provide a comprehensive analysis in the following JSON format:

{
  "summary": "Brief 2-3 sentence summary of what this contract does",
  "purpose": "Main purpose/use case of the contract",
  "risk_level": "low|medium|high|critical",
  "risk_factors": ["List of potential risks or concerns"],
  "key_functions": ["List of important functions"],
  "token_info": {
    "is_token": true/false,
    "token_type": "ERC20|ERC721|ERC1155|null",
    "features": ["mintable", "burnable", etc.]
  }
}

Focus on:
1. What the contract does
2. Security risks and concerns
3. Key functionality
4. Token standards if applicable
5. Upgrade mechanisms if present

Respond ONLY with valid JSON."""

        return prompt

    def _build_wallet_prompt(self, wallet_data: Dict[str, Any], chain: str) -> str:
        """Build prompt for wallet analysis."""
        transactions = wallet_data.get("transactions", [])
        tokens = wallet_data.get("tokens", {})

        prompt = f"""Analyze this wallet on {chain}:

Address: {wallet_data['address']}
Balance: {wallet_data.get('balance', '0')} Wei
Total Transactions: {len(transactions)}
Token Types Held: {len(tokens)}

Recent Transaction Summary:
"""

        for i, tx in enumerate(transactions[:20], 1):
            prompt += f"{i}. {tx.get('method', 'transfer')} - Value: {tx['value']} - {tx['timestamp']}\n"

        if tokens:
            prompt += f"\nTokens:\n"
            for token_addr, token_info in list(tokens.items())[:10]:
                prompt += f"- {token_info.get('name', 'Unknown')} ({token_info.get('symbol', '???')})\n"

        prompt += """
Please analyze and provide response in JSON format:

{
  "summary": "Brief summary of wallet activity and holdings",
  "activity_pattern": "Description of transaction patterns",
  "wallet_type": "DeFi user|NFT collector|Exchange|Bot|Contract|Normal user",
  "notable_interactions": ["List of interesting contracts or protocols interacted with"]
}

Focus on:
1. Main wallet activities
2. Type of user behavior
3. DeFi protocols used
4. NFT or token collecting patterns
5. Any unusual or notable behavior

Respond ONLY with valid JSON."""

        return prompt

    def _build_transaction_prompt(self, tx_data: Dict[str, Any], chain: str) -> str:
        """Build prompt for transaction analysis."""
        prompt = f"""Analyze this transaction on {chain}:

Hash: {tx_data['hash']}
From: {tx_data['from']}
To: {tx_data.get('to', 'Contract Creation')}
Value: {tx_data['value']} Wei
Input Data: {tx_data.get('input', '0x')[:200]}...
Status: {'Success' if tx_data.get('receipt', {}).get('status', True) else 'Failed'}

Logs: {len(tx_data.get('receipt', {}).get('logs', []))} events

Please provide analysis in JSON format:

{
  "explanation": "Human-readable explanation of what this transaction does",
  "method_name": "Name of function called (if identifiable)",
  "parameters": {"param1": "value1"},
  "risks": ["List any risks or concerns"]
}

Respond ONLY with valid JSON."""

        return prompt

    def _parse_contract_analysis(self, text: str) -> Dict[str, Any]:
        """Parse contract analysis from Claude response."""
        try:
            # Try to extract JSON from response
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # Fallback: return basic structure
        return {
            "summary": text[:500],
            "purpose": "Analysis parsing failed",
            "risk_level": "unknown",
            "risk_factors": [],
            "key_functions": [],
        }

    def _parse_wallet_analysis(self, text: str) -> Dict[str, Any]:
        """Parse wallet analysis from Claude response."""
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {
            "summary": text[:500],
            "activity_pattern": "Unknown",
            "wallet_type": "Unknown",
            "notable_interactions": [],
        }

    def _parse_transaction_analysis(self, text: str) -> Dict[str, Any]:
        """Parse transaction analysis from Claude response."""
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return {
            "explanation": text[:500],
            "method_name": None,
            "parameters": {},
            "risks": [],
        }

    def _call_ai(self, prompt: str) -> str:
        """
        Call AI provider (OpenAI or Anthropic) and return response text.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            The AI's response as text
            
        Raises:
            AIAnalysisError: If the AI call fails
        """
        try:
            logger.debug(f"Calling {self.provider} API (model: {self.model})")
            
            if self.provider == "openai":
                from openai import OpenAIError
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=self.max_tokens,
                        temperature=0.7,
                    )
                    result = response.choices[0].message.content
                    logger.debug(f"OpenAI API call successful ({len(result)} chars)")
                    return result
                except OpenAIError as e:
                    logger.error(f"OpenAI API error: {e}")
                    raise AIAnalysisError(f"OpenAI API failed: {e}") from e
            
            else:  # anthropic
                from anthropic import APIError
                try:
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    result = response.content[0].text
                    logger.debug(f"Anthropic API call successful ({len(result)} chars)")
                    return result
                except APIError as e:
                    logger.error(f"Anthropic API error: {e}")
                    raise AIAnalysisError(f"Anthropic API failed: {e}") from e
                    
        except ImportError as e:
            logger.error(f"Failed to import AI provider: {e}")
            raise AIAnalysisError(f"AI provider library not available: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error calling AI: {e}")
            raise AIAnalysisError(f"AI call failed: {e}") from e
