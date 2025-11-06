# ChainXplain 🔗✨

AI-powered blockchain analysis toolkit that makes understanding smart contracts, wallets, and transactions as easy as asking a question.

[![CI](https://github.com/bharathpreetham-lilly/chainxplain/workflows/CI/badge.svg)](https://github.com/bharathpreetham-lilly/chainxplain/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/bharathpreetham-lilly/chainxplain/branch/main/graph/badge.svg)](https://codecov.io/gh/bharathpreetham-lilly/chainxplain)
[![PyPI version](https://badge.fury.io/py/chainxplain.svg)](https://badge.fury.io/py/chainxplain)
[![Python](https://img.shields.io/pypi/pyversions/chainxplain.svg)](https://pypi.org/project/chainxplain/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 What Can You Do With ChainXplain?

ChainXplain uses AI (ChatGPT or Claude) to analyze blockchain data and provide human-readable explanations. Perfect for:

- 🔍 **Understanding Smart Contracts** - Get plain English explanations of what contracts do
- 💰 **Wallet Analysis** - Analyze wallet behavior, holdings, and transaction patterns  
- 🔄 **Transaction Decoding** - Understand what happened in complex transactions
- 🪙 **Token Research** - Get detailed information about any ERC-20 token
- 🛡️ **Security Insights** - Identify potential risks and security concerns

**Three ways to use it:**
- 🐍 Python Library
- 🤖 MCP Server (for AI agents like Claude Desktop)
- ⌨️ Command-Line Interface

---

## 🚀 Quick Start

### 1. Install

```bash
# Using pip
pip install chainxplain

# Using Poetry (recommended)
git clone https://github.com/bharathpreetham-lilly/chainxplain.git
cd chainxplain
poetry install -E openai  # If using ChatGPT
```

### 2. Configure API Keys

Edit `.env` file in the project root:

```bash
# Choose your AI provider (required - pick ONE)
OPENAI_API_KEY=sk-your-key-here          # For ChatGPT (recommended)
# or
ANTHROPIC_API_KEY=sk-ant-your-key-here   # For Claude

# Optional but recommended  
ALCHEMY_API_KEY=your-alchemy-key         # Better RPC reliability
ETHERSCAN_API_KEY=your-etherscan-key     # Contract source code access
```

**Get API Keys:**
- 🔑 OpenAI: https://platform.openai.com/api-keys
- 🔑 Anthropic: https://console.anthropic.com/
- 🔑 Alchemy: https://dashboard.alchemy.com/
- 🔑 Etherscan: https://etherscan.io/myapikey

### 3. Try It Out

```bash
# Run the demo (works without AI keys)
poetry run python demo.py

# Analyze USDC contract (needs AI key)
poetry run chainxplain explain 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --chain ethereum
```

---

## 📚 Usage Examples

### 🔍 Analyze Smart Contracts

**Example: Analyze USDC Token Contract**
```bash
poetry run chainxplain explain 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --chain ethereum
```

**Output:**
```
🔍 Analyzing contract on ethereum...

Contract Analysis Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:           USD Coin
Purpose:        Stablecoin pegged to USD
Risk Level:     LOW
Verified:       ✓ Yes

📝 Summary:
USDC is a fully-backed stablecoin issued by Circle. The contract 
implements the ERC-20 standard with additional features like 
minting, burning, and blacklisting capabilities.

🔑 Key Functions:
  • transfer - Transfer tokens between addresses
  • approve - Approve spending allowance  
  • mint - Create new tokens (admin only)
  • burn - Destroy tokens
  • blacklist - Block addresses (admin only)

⚠️ Risk Assessment:
  ✓ Contract is verified on Etherscan
  ✓ Widely used and audited
  ⚠ Centralized control (admin functions)
  ✓ No known vulnerabilities

💰 Token Info:
  Symbol:       USDC
  Decimals:     6
  Total Supply: 51,684,406,139.57 USDC
```

**More Examples:**

```bash
# Analyze Uniswap V3 Router
poetry run chainxplain explain 0xE592427A0AEce92De3Edee1F18E0157C05861564 --chain ethereum

# Check a suspicious contract
poetry run chainxplain explain 0x... --chain ethereum --verbose
```

### 💰 Wallet Analysis

**Example: Analyze Vitalik's Wallet**
```bash
poetry run chainxplain wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --chain ethereum
```

**Output includes:**
- Native ETH balance  
- Token holdings (ERC-20, ERC-721)
- Transaction history and patterns
- Wallet behavior classification
- Notable contract interactions

**More Examples:**

```bash
# Check any wallet on different chains
poetry run chainxplain wallet 0x... --chain polygon
poetry run chainxplain wallet 0x... --chain arbitrum
poetry run chainxplain wallet 0x... --chain base

# Get detailed analysis
poetry run chainxplain wallet 0x... --chain ethereum --verbose
```

### 🔄 Transaction Analysis

**Example: Decode a Transaction**
```bash
poetry run chainxplain tx 0x1234567890abcdef... --chain ethereum
```

**Output includes:**
- Transaction status and details
- Gas used and transaction cost
- Decoded function call and parameters
- Token transfers that occurred
- AI explanation of what happened

**More Examples:**

```bash
# Understand a Uniswap swap
poetry run chainxplain tx 0x... --chain ethereum

# Decode NFT purchase
poetry run chainxplain tx 0x... --chain ethereum

# Analyze flash loan transaction
poetry run chainxplain tx 0x... --chain ethereum --verbose
```

### 🪙 Token Information

**Example: Research a Token**
```bash
poetry run chainxplain token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --chain ethereum
```

**Output includes:**
- Token name, symbol, decimals
- Total supply  
- Contract verification status
- Security analysis
- Usage patterns

---

## 🐍 Python Library Usage

### Basic Contract Analysis

```python
from chainxplain import ChainExplainClient

# Initialize client (reads from .env)
client = ChainExplainClient()

# Analyze a contract
analysis = client.analyze_contract(
    address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
    chain="ethereum"
)

print(f"Contract: {analysis.name}")
print(f"Purpose: {analysis.purpose}")
print(f"Risk Level: {analysis.risk_level}")
print(f"Summary: {analysis.summary}")
print(f"Key Functions: {', '.join(analysis.key_functions)}")

# Check token info if it's a token contract
if analysis.token_info:
    print(f"Symbol: {analysis.token_info['symbol']}")
    print(f"Total Supply: {analysis.token_info['totalSupply']}")
```

### Wallet Analysis

```python
from chainxplain import analyze_wallet

# Quick wallet analysis (convenience function)
wallet = analyze_wallet(
    address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    chain="ethereum"
)

print(f"Balance: {wallet.native_balance} ETH")
print(f"Total Transactions: {wallet.total_transactions}")
print(f"Wallet Type: {wallet.wallet_type}")
print(f"Activity Pattern: {wallet.activity_pattern}")

# Check token holdings
for token, amount in wallet.token_holdings.items():
    print(f"  {token}: {amount}")

# View recent transactions
for tx in wallet.recent_transactions[:5]:
    print(f"  {tx.hash}: {tx.method} - {tx.value} ETH")
```

### Transaction Decoding

```python
client = ChainExplainClient()

# Analyze a complex transaction
tx = client.analyze_transaction(
    tx_hash="0x123...",
    chain="ethereum"
)

print(f"From: {tx.from_address}")
print(f"To: {tx.to_address}")
print(f"Value: {tx.value} ETH")
print(f"Gas Used: {tx.gas_used}")
print(f"Status: {'✓ Success' if tx.status else '✗ Failed'}")
print(f"\nExplanation:\n{tx.explanation}")
```

### Batch Analysis

```python
from chainxplain import ChainExplainClient

client = ChainExplainClient()

# Analyze multiple contracts
stablecoins = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
}

for name, address in stablecoins.items():
    analysis = client.analyze_contract(address, "ethereum")
    print(f"{name}: {analysis.summary[:100]}...")
```

### Custom Configuration

```python
from chainxplain import ChainExplainClient

# Initialize with specific keys (overrides .env)
client = ChainExplainClient(
    openai_api_key="sk-...",           # Use ChatGPT
    alchemy_api_key="...",             # Better RPC  
    etherscan_api_key="..."            # Contract source
)

# Use on different chains
ethereum_contract = client.analyze_contract("0x...", "ethereum")
polygon_contract = client.analyze_contract("0x...", "polygon")
arbitrum_wallet = client.analyze_wallet("0x...", "arbitrum")
```

---

## 🤖 MCP Server (AI Agent Integration)

Use ChainXplain as a tool for AI agents like Claude Desktop.

### Start the Server

```bash
poetry run chainxplain-mcp
```

### Available MCP Tools

The server exposes these tools to AI agents:

- **`analyze_contract`** - Analyze any smart contract
- **`analyze_wallet`** - Get wallet insights and activity
- **`get_transaction_details`** - Decode and explain transactions
- **`get_token_info`** - Get token information
- **`check_contract_security`** - Security risk assessment

### Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chainxplain": {
      "command": "poetry",
      "args": ["run", "chainxplain-mcp"],
      "cwd": "/path/to/chainxplain",
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "ALCHEMY_API_KEY": "...",
        "ETHERSCAN_API_KEY": "..."
      }
    }
  }
}
```

Then restart Claude Desktop and ask questions like:
- "Analyze the USDC contract on Ethereum"
- "What tokens does vitalik.eth hold?"
- "Explain this transaction: 0x..."

---

## 🎯 Real-World Use Cases

### 1. Due Diligence on New Token

```bash
# Step 1: Analyze the token contract
poetry run chainxplain explain 0x... --chain ethereum

# Step 2: Check the creator's wallet  
poetry run chainxplain wallet 0x... --chain ethereum

# Step 3: Review recent transactions
poetry run chainxplain tx 0x... --chain ethereum
```

### 2. Understand DeFi Protocol

```python
from chainxplain import ChainExplainClient

client = ChainExplainClient()

# Analyze core protocol contracts
router = client.analyze_contract("0xE592427A0AEce92De3Edee1F18E0157C05861564", "ethereum")
print(f"Uniswap Router: {router.summary}")

# Check liquidity pools
pool = client.analyze_contract("0x...", "ethereum")
print(f"Pool purpose: {pool.purpose}")
```

### 3. Track Whale Wallets

```bash
# Monitor large holders
poetry run chainxplain wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --verbose

# Analyze their recent activity
poetry run chainxplain wallet 0x... --chain ethereum
```

### 4. Security Research

```python
from chainxplain import ChainExplainClient

client = ChainExplainClient()

# Check contract for risks
analysis = client.analyze_contract("0x...", "ethereum")

if analysis.risk_level in ["high", "critical"]:
    print(f"⚠️ Warning: {analysis.risk_level} risk detected!")
    print(f"Risk factors:")
    for risk in analysis.risk_factors:
        print(f"  - {risk}")
else:
    print(f"✓ Risk level: {analysis.risk_level}")
```

### 5. Multi-Chain Portfolio Tracking

```python
from chainxplain import ChainExplainClient

client = ChainExplainClient()

wallet_address = "0x..."
chains = ["ethereum", "polygon", "arbitrum", "optimism"]

print(f"Portfolio for {wallet_address}:\n")

for chain in chains:
    wallet = client.analyze_wallet(wallet_address, chain)
    print(f"{chain.upper()}:")
    print(f"  Balance: {wallet.native_balance}")
    print(f"  Tokens: {len(wallet.token_holdings)}")
    print(f"  Activity: {wallet.activity_pattern}")
    print()
```

---

## 🌐 Supported Blockchains

ChainXplain supports 6+ blockchain networks:

```bash
# Ethereum Mainnet
--chain ethereum

# Polygon (formerly Matic)
--chain polygon

# Arbitrum One (L2)
--chain arbitrum

# Optimism (L2)
--chain optimism

# Base (Coinbase L2)
--chain base

# BNB Smart Chain
--chain bsc
```

Each chain has unique characteristics:
- **Ethereum**: Most contracts, highest security, higher gas fees
- **Polygon**: Fast & cheap, gaming/NFT focused
- **Arbitrum/Optimism**: L2 scaling, DeFi focused
- **Base**: New L2, growing ecosystem
- **BSC**: Low fees, high throughput

---

## ⚙️ Configuration Reference

All settings in `.env` file:

```bash
# ============================================================================
# AI Provider (REQUIRED - choose ONE)
# ============================================================================
OPENAI_API_KEY=sk-...          # ChatGPT (GPT-4o) - Recommended
# or
ANTHROPIC_API_KEY=sk-ant-...   # Claude (3.5 Sonnet)

# ============================================================================
# Blockchain APIs (Optional but recommended)
# ============================================================================
ALCHEMY_API_KEY=...            # Enhanced RPC & better reliability
ETHERSCAN_API_KEY=...          # Ethereum contract source code
POLYGONSCAN_API_KEY=...        # Polygon contracts
ARBISCAN_API_KEY=...           # Arbitrum contracts
OPTIMISTIC_ETHERSCAN_API_KEY=...  # Optimism contracts
BASESCAN_API_KEY=...           # Base contracts
BSCSCAN_API_KEY=...            # BSC contracts

# ============================================================================
# Custom RPC Endpoints (Optional)
# ============================================================================
ETHEREUM_RPC_URL=https://...   # Custom Ethereum RPC
POLYGON_RPC_URL=https://...    # Custom Polygon RPC
ARBITRUM_RPC_URL=https://...   # Custom Arbitrum RPC

# ============================================================================
# Advanced Settings (Optional)
# ============================================================================
CACHE_TTL=3600                 # Cache duration in seconds
RATE_LIMIT=5                   # API requests per second
MAX_TOKENS=4096                # Max AI response tokens
DEFAULT_CHAIN=ethereum         # Default blockchain
```

---

## 🧪 Testing & Development

```bash
# Clone repository
git clone https://github.com/bharathpreetham-lilly/chainxplain.git
cd chainxplain

# Install dependencies
poetry install --with dev -E openai

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=chainxplain

# Run integration tests (needs API keys)
poetry run pytest tests/integration/ --run-integration

# Code quality checks
poetry run black src/ tests/
poetry run ruff check src/ tests/
poetry run mypy src/
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ChainXplain                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Python Library          MCP Server          CLI        │
│  ├─ ChainExplainClient  ├─ FastMCP Tools   ├─ Typer    │
│  ├─ analyze_contract()  ├─ 5 Tools         ├─ Rich UI  │
│  └─ analyze_wallet()    └─ 2 Resources     └─ Commands │
│                                                          │
├─────────────────────────────────────────────────────────┤
│               Core Components                            │
│  ├─ AI Analyzer (ChatGPT/Claude)                        │
│  ├─ Blockchain Clients (Web3, Alchemy)                  │
│  ├─ Explorer Integration (Etherscan APIs)               │
│  └─ Data Models (Pydantic)                              │
│                                                          │
├─────────────────────────────────────────────────────────┤
│             External Services                            │
│  ├─ OpenAI/Anthropic (AI Analysis)                      │
│  ├─ Alchemy (Enhanced Blockchain APIs)                  │
│  ├─ Etherscan (Contract Verification)                   │
│  └─ Public RPCs (Fallback)                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick Start for Contributors:**

```bash
# Fork and clone
git clone https://github.com/your-username/chainxplain.git
cd chainxplain

# Setup
poetry install --with dev -E all
poetry run pre-commit install

# Make changes and test
poetry run pytest
poetry run black src/ tests/
poetry run mypy src/

# Submit PR
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-4o for intelligent analysis
- **Anthropic** - Claude 3.5 Sonnet AI
- **Alchemy** - Enhanced blockchain APIs
- **Etherscan** - Blockchain explorer data
- **FastMCP** - Modern MCP implementation

---

## 🌟 Features at a Glance

✅ Multi-chain support (6+ networks)  
✅ Dual AI provider (ChatGPT & Claude)  
✅ Smart contract analysis  
✅ Wallet behavior tracking  
✅ Transaction decoding  
✅ Token information  
✅ Security risk assessment  
✅ MCP server for AI agents  
✅ Python library & CLI  
✅ Rich terminal output  
✅ Comprehensive caching  
✅ Rate limiting  
✅ Type hints & validation  

---

**Made with ❤️ for the blockchain community**