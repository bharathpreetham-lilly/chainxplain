# ChainXplain 🔗✨

**Production-Grade AI-powered blockchain analysis toolkit** that makes understanding smart contracts, wallets, and transactions as easy as asking a question.

[![CI](https://github.com/bharathpreetham-lilly/chainxplain/workflows/CI/badge.svg)](https://github.com/bharathpreetham-lilly/chainxplain/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/bharathpreetham-lilly/chainxplain/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/bharathpreetham-lilly/chainxplain)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bharathpreetham-lilly/chainxplain/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20%7C%20Anthropic-74aa9c)](https://openai.com)
[![Chains](https://img.shields.io/badge/chains-6%2B-627EEA?logo=ethereum&logoColor=white)](https://ethereum.org)

> **Note:** This package is currently in development. PyPI publication coming soon!

---

## 🌟 What Can You Do With ChainXplain?

ChainXplain uses AI (ChatGPT or Claude) to analyze blockchain data and provide human-readable explanations with **enterprise-grade features**:

- 🔍 **Smart Contract Analysis** - AI-powered explanations with security scanning
- 💰 **Wallet Analysis** - Track behavior, holdings, and transaction patterns  
- 🔄 **Transaction Decoding** - Understand complex DeFi transactions
- 🪙 **Token Research** - Detailed ERC-20 token information
- 🛡️ **Security Analysis** - Automated vulnerability detection & risk scoring
- 📊 **Export Reports** - Generate JSON, CSV, and Markdown reports
- 🌐 **REST API** - Production-ready FastAPI server
- ⚡ **Rate Limiting** - Built-in API rate limiting enforcement
- ✅ **Input Validation** - Enterprise-grade security validation

**Four ways to use it:**
- 🐍 Python Library
- 🌐 REST API Server
- 🤖 MCP Server (for AI agents like Claude Desktop)
- ⌨️ Command-Line Interface

---

## 🚀 Quick Start

### 1. Install

```bash
# Using pip
pip install chainxplain

# Using Poetry (recommended for development)
git clone https://github.com/bharathpreetham-lilly/chainxplain.git
cd chainxplain
poetry install -E openai  # If using ChatGPT
```

### 2. Configure API Keys

Create a `.env` file in the project root:

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

# Start REST API server
poetry run python run_api.py
# Then visit: http://localhost:8000/docs
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
from chainxplain import ChainXplain, ChainConfig

# Initialize client (automatically reads from .env)
client = ChainXplain(
    ai_provider="openai",  # or "anthropic"
    chain=ChainConfig.ETHEREUM
)

# Analyze a contract with security scanning
analysis = client.analyze_contract(
    address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
)

print(f"Contract: {analysis.name}")
print(f"Purpose: {analysis.purpose}")
print(f"Risk Level: {analysis.risk_level}")
print(f"Security Score: {analysis.security_score}/100")
print(f"Summary: {analysis.summary}")

# Check for vulnerabilities
if analysis.vulnerabilities:
    print("\n⚠️ Security Issues Found:")
    for vuln in analysis.vulnerabilities:
        print(f"  - {vuln['severity']}: {vuln['title']}")
        print(f"    {vuln['description']}")

# Export analysis to multiple formats
from chainxplain.export import ReportExporter

exporter = ReportExporter()
exporter.export_to_markdown(analysis, "usdc_analysis.md")  # Beautiful report
exporter.export_to_json(analysis, "usdc_analysis.json")    # Machine-readable
exporter.export_to_csv(analysis, "usdc_analysis.csv")      # Spreadsheet

# Files saved to ./reports/ directory
```

### Wallet Analysis

```python
# Analyze a wallet with transaction history
wallet = client.analyze_wallet(
    address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    limit=100  # Max 1000 transactions
)

print(f"Balance: {wallet.balance_eth} ETH")
print(f"Total Transactions: {len(wallet.transactions)}")
print(f"Holdings: {len(wallet.holdings)} tokens")

# Check token holdings
for holding in wallet.holdings:
    print(f"  {holding['symbol']}: {holding['balance']} (${holding['value_usd']})")

# View recent activity
for tx in wallet.transactions[:5]:
    print(f"  {tx.hash}: {tx.function_name} - {tx.value} ETH")

# Export wallet report
exporter.export_to_markdown(wallet, "vitalik_wallet_analysis.md")
```

### Security Analysis

```python
from chainxplain.ai.security import SecurityAnalyzer

# Run dedicated security scan
security_analyzer = SecurityAnalyzer()

# Analyze contract source code (if verified)
report = security_analyzer.analyze_contract(
    source_code=analysis.source_code,
    contract_name=analysis.name
)

print(f"\n🔒 Security Report for {analysis.name}")
print(f"Overall Score: {report.overall_score}/100")
print(f"Risk Level: {report.risk_level}")

# Review detected vulnerabilities
for issue in report.vulnerabilities:
    print(f"\n⚠️ {issue['severity'].upper()}: {issue['title']}")
    print(f"   Pattern: {issue['pattern']}")
    print(f"   Description: {issue['description']}")
    print(f"   Recommendation: {issue['recommendation']}")

# Common vulnerabilities detected:
# - Reentrancy attacks
# - Unchecked external calls
# - tx.origin authentication
# - Block timestamp manipulation
# - Integer overflow/underflow
# - Access control issues
# - DoS vulnerabilities
```

### REST API Integration

```python
import requests

# Analyze contract via API
response = requests.post(
    "http://localhost:8000/analyze/contract",
    json={
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "chain": "ethereum"
    }
)

data = response.json()
print(f"Status: {data['status']}")
print(f"Contract: {data['data']['name']}")
print(f"Security Score: {data['data']['security_score']}")

# Analyze wallet via GET request
response = requests.get(
    "http://localhost:8000/analyze/wallet/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    params={"chain": "ethereum", "limit": 50}
)

wallet_data = response.json()['data']
print(f"Balance: {wallet_data['balance_eth']} ETH")
print(f"Holdings: {len(wallet_data['holdings'])} tokens")
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

## 🌐 REST API Server

ChainXplain includes a production-ready FastAPI server for integration with web applications, mobile apps, or microservices.

### Start the Server

```bash
# Start with hot reload (development)
poetry run python run_api.py

# Or start with uvicorn directly
poetry run uvicorn chainxplain.api.server:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: **http://localhost:8000**  
API docs: **http://localhost:8000/docs** (Swagger UI)  
Alternative docs: **http://localhost:8000/redoc**

### Available Endpoints

#### 🔍 Contract Analysis
```bash
# POST request
curl -X POST http://localhost:8000/analyze/contract \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "chain": "ethereum"
  }'

# GET request
curl "http://localhost:8000/analyze/contract/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48?chain=ethereum"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "name": "USD Coin",
    "symbol": "USDC",
    "chain": "ethereum",
    "security_score": 95,
    "risk_level": "low",
    "vulnerabilities": [],
    "is_verified": true,
    "source_code": "...",
    "ai_insights": "USDC is a fully-backed stablecoin...",
    "key_functions": ["transfer", "approve", "mint", "burn"]
  }
}
```

#### 💰 Wallet Analysis
```bash
# POST request
curl -X POST http://localhost:8000/analyze/wallet \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "chain": "ethereum",
    "limit": 50
  }'

# GET request (recommended)
curl "http://localhost:8000/analyze/wallet/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045?chain=ethereum&limit=50"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "chain": "ethereum",
    "balance_eth": "1234.56",
    "holdings": [
      {
        "symbol": "USDC",
        "balance": "10000.00",
        "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "value_usd": 10000.00
      }
    ],
    "total_transactions": 150,
    "ai_insights": "Active DeFi user with diverse holdings..."
  }
}
```

#### 🔄 Transaction Analysis
```bash
curl -X POST http://localhost:8000/analyze/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "tx_hash": "0x1234...abcd",
    "chain": "ethereum"
  }'
```

#### 🏥 Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "ai_provider": "openai",
  "supported_chains": ["ethereum", "polygon", "arbitrum", "optimism", "base"]
}
```

### Error Handling

**400 Bad Request** - Invalid input:
```json
{
  "status": "error",
  "message": "Invalid Ethereum address format. Must be 42 characters starting with 0x"
}
```

**500 Internal Server Error** - Analysis failed:
```json
{
  "status": "error",
  "message": "Failed to analyze contract: API rate limit exceeded"
}
```

### Production Deployment

```bash
# Use gunicorn for production
pip install gunicorn
gunicorn chainxplain.api.server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# Or with Docker
docker build -t chainxplain-api .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e ALCHEMY_API_KEY=your-key \
  chainxplain-api
```

### API Features

✅ **CORS Enabled** - Works with web frontends  
✅ **Input Validation** - Prevents invalid addresses/hashes  
✅ **Rate Limiting** - 5 AI calls per minute enforced  
✅ **Comprehensive Logging** - All requests logged with timestamps  
✅ **Auto Documentation** - Interactive Swagger UI at `/docs`  
✅ **Type Safety** - Pydantic models for all requests/responses  
✅ **Error Recovery** - Graceful handling of API failures

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

### 1. Security Audit Before Token Purchase

```bash
# Step 1: Analyze the token contract with security scanning
poetry run chainxplain explain 0x... --chain ethereum

# Output includes:
# - Security score (0-100)
# - Detected vulnerabilities (reentrancy, overflow, etc.)
# - Risk level assessment
# - Code verification status
```

```python
from chainxplain import ChainXplain
from chainxplain.ai.security import SecurityAnalyzer

client = ChainXplain()

# Get contract analysis with security
analysis = client.analyze_contract("0x...", "ethereum")

print(f"Security Score: {analysis.security_score}/100")
print(f"Risk Level: {analysis.risk_level}")

if analysis.vulnerabilities:
    print("\n⚠️ SECURITY ISSUES FOUND:")
    for vuln in analysis.vulnerabilities:
        print(f"  {vuln['severity']}: {vuln['title']}")
        
# Export detailed security report
from chainxplain.export import ReportExporter
exporter = ReportExporter()
exporter.export_to_markdown(analysis, "security_audit.md")
```

### 2. Track and Analyze Whale Wallets

```python
from chainxplain import ChainXplain
from chainxplain.export import ReportExporter

client = ChainXplain()
exporter = ReportExporter()

# Analyze whale wallet
whale = client.analyze_wallet(
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",  # Vitalik
    limit=500
)

print(f"Balance: {whale.balance_eth} ETH")
print(f"Total Holdings: ${sum(h['value_usd'] for h in whale.holdings):,.2f}")

# Export detailed holdings report
exporter.export_to_csv(whale, "whale_holdings.csv")
exporter.export_to_markdown(whale, "whale_report.md")

# Track activity patterns
print(f"Recent activity: {len(whale.transactions)} transactions")
```

### 3. DeFi Protocol Research

```python
from chainxplain import ChainXplain

client = ChainXplain()

# Analyze Uniswap V3 Router
router = client.analyze_contract(
    "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "ethereum"
)

print(f"Protocol: {router.name}")
print(f"Purpose: {router.purpose}")
print(f"Key Functions: {router.key_functions}")
print(f"Security Score: {router.security_score}/100")

# Check for known vulnerabilities
if router.vulnerabilities:
    print("\n⚠️ Security concerns:")
    for issue in router.vulnerabilities:
        print(f"  - {issue['title']}")
else:
    print("\n✅ No major security issues detected")
```

### 4. Automated Security Monitoring via API

```python
import requests
import time

# Monitor multiple contracts via REST API
contracts_to_monitor = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F"
}

for name, address in contracts_to_monitor.items():
    response = requests.post(
        "http://localhost:8000/analyze/contract",
        json={"address": address, "chain": "ethereum"}
    )
    
    data = response.json()['data']
    
    print(f"\n{name}:")
    print(f"  Security Score: {data['security_score']}/100")
    print(f"  Risk Level: {data['risk_level']}")
    
    if data['vulnerabilities']:
        print(f"  ⚠️ Issues: {len(data['vulnerabilities'])} found")
        # Send alert to monitoring system
    
    time.sleep(12)  # Respect rate limits (5/min)
```

### 5. Multi-Chain Portfolio Analysis

```python
from chainxplain import ChainXplain, ChainConfig
from chainxplain.export import ReportExporter

client = ChainXplain()
exporter = ReportExporter()

wallet_address = "0x..."
chains = [
    ChainConfig.ETHEREUM,
    ChainConfig.POLYGON,
    ChainConfig.ARBITRUM,
    ChainConfig.OPTIMISM,
    ChainConfig.BASE
]

print(f"Portfolio Analysis for {wallet_address}\n")
print("=" * 60)

total_value_usd = 0

for chain in chains:
    client.chain = chain
    wallet = client.analyze_wallet(wallet_address, limit=100)
    
    chain_value = sum(h.get('value_usd', 0) for h in wallet.holdings)
    total_value_usd += chain_value
    
    print(f"\n{chain.name.upper()}:")
    print(f"  Native Balance: {wallet.balance_eth}")
    print(f"  Token Holdings: {len(wallet.holdings)}")
    print(f"  Total Value: ${chain_value:,.2f}")
    print(f"  Transactions: {len(wallet.transactions)}")
    
    # Export per-chain report
    exporter.export_to_json(
        wallet,
        f"portfolio_{chain.name.lower()}.json"
    )

print(f"\n{'=' * 60}")
print(f"TOTAL PORTFOLIO VALUE: ${total_value_usd:,.2f}")
```

### 6. Transaction Forensics

```bash
# Investigate suspicious transaction
poetry run chainxplain tx 0x1234...abcd --chain ethereum --verbose

# Output includes:
# - Decoded function call and parameters
# - Token transfers (even internal ones)
# - Event logs decoded
# - Gas analysis
# - AI explanation of what happened
```

```python
from chainxplain import ChainXplain

client = ChainXplain()

# Deep dive into transaction
tx = client.analyze_transaction("0x...", "ethereum")

print(f"Function Called: {tx.function_name}")
print(f"Status: {tx.status}")
print(f"Gas Used: {tx.gas_used} ({tx.gas_price} Gwei)")

# Check for suspicious patterns
if "approve" in tx.function_name.lower():
    print("⚠️ Token approval detected - verify spender address!")
    
if tx.value > 10:  # More than 10 ETH
    print(f"⚠️ Large transfer: {tx.value} ETH")
```

---

## 🔒 Security Features

ChainXplain includes enterprise-grade security analysis to help you identify vulnerabilities before they become exploits.

### Automated Vulnerability Detection

The built-in security analyzer scans for **6+ common vulnerability patterns**:

1. **Reentrancy Attacks** - Detects unsafe external calls that could enable reentrancy
2. **Unchecked External Calls** - Flags `delegatecall` and low-level calls without validation
3. **tx.origin Authentication** - Identifies improper use of `tx.origin` for access control
4. **Block Timestamp Manipulation** - Warns about reliance on `block.timestamp`
5. **Selfdestruct Usage** - Detects potentially dangerous `selfdestruct` calls
6. **Unprotected Ether Withdrawal** - Finds functions that transfer ETH without access control
7. **Integer Overflow/Underflow** - Checks for SafeMath or Solidity 0.8+ usage
8. **Access Control Issues** - Verifies presence of `onlyOwner` or `require` statements
9. **DoS Vulnerabilities** - Detects unbounded loops that could cause gas exhaustion

### Security Scoring System

Every contract receives a **security score from 0-100**:

- **90-100**: Excellent - Well-audited, minimal risk
- **70-89**: Good - Minor concerns, generally safe
- **50-69**: Moderate - Some issues, use with caution
- **30-49**: Poor - Multiple vulnerabilities detected
- **0-29**: Critical - Severe security flaws, avoid using

### How to Use Security Features

**Via CLI:**
```bash
# Security analysis is automatic in all contract analyses
poetry run chainxplain explain 0xContractAddress --chain ethereum

# Output includes:
# - Security Score: 95/100
# - Risk Level: low
# - Detected Vulnerabilities: [list]
# - Recommendations: [security tips]
```

**Via Python:**
```python
from chainxplain import ChainXplain
from chainxplain.ai.security import SecurityAnalyzer

client = ChainXplain()

# Analyze contract (includes security scan)
analysis = client.analyze_contract("0x...", "ethereum")

print(f"Security Score: {analysis.security_score}/100")
print(f"Risk Level: {analysis.risk_level}")

# Check for specific vulnerabilities
if analysis.vulnerabilities:
    print("\n⚠️ SECURITY ISSUES DETECTED:")
    for vuln in analysis.vulnerabilities:
        print(f"\n{vuln['severity'].upper()}: {vuln['title']}")
        print(f"Pattern: {vuln['pattern']}")
        print(f"Description: {vuln['description']}")
        print(f"Recommendation: {vuln['recommendation']}")

# Run dedicated security analysis
security_analyzer = SecurityAnalyzer()
security_report = security_analyzer.analyze_contract(
    source_code=analysis.source_code,
    contract_name=analysis.name
)

print(f"\nDetailed Security Report:")
print(f"Overall Score: {security_report.overall_score}/100")
print(f"Risk Level: {security_report.risk_level}")
print(f"Issues Found: {len(security_report.vulnerabilities)}")
```

**Via REST API:**
```bash
curl -X POST http://localhost:8000/analyze/contract \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xContractAddress",
    "chain": "ethereum"
  }' | jq '.data.security_score'
```

### Example Security Report

```
🔒 Security Analysis for USD Coin (USDC)

Overall Security Score: 95/100
Risk Level: LOW

✅ Strengths:
  • Contract verified on Etherscan
  • Uses Solidity 0.8+ (overflow protection)
  • Proper access control with onlyOwner modifiers
  • No reentrancy vulnerabilities detected
  • Well-audited by multiple firms

⚠️ Considerations:
  • Centralized control (admin can mint/burn)
  • Blacklist function (addresses can be blocked)
  • Upgradeable proxy pattern (code can change)

📋 Recommendations:
  • Monitor admin key security
  • Review audit reports before large transactions
  • Consider multi-sig for admin functions
```

### Security Best Practices

When using ChainXplain for security analysis:

1. **Always verify source code** - Unverified contracts get lower scores
2. **Cross-reference with audits** - ChainXplain complements, not replaces, professional audits
3. **Check historical issues** - Look for past exploits or vulnerabilities
4. **Monitor contract updates** - Re-analyze after upgrades
5. **Export reports** - Save security analyses for compliance/documentation

```python
from chainxplain.export import ReportExporter

# Generate comprehensive security report
exporter = ReportExporter()
exporter.export_to_markdown(analysis, "security_audit_report.md")
exporter.export_to_json(analysis, "security_data.json")
```

---

## 📊 Export & Reporting

ChainXplain can export analysis results in **three formats** for different use cases:

### 1. JSON Export (Machine-Readable)

Perfect for: APIs, databases, automated processing, data pipelines

```python
from chainxplain import ChainXplain
from chainxplain.export import ReportExporter

client = ChainXplain()
exporter = ReportExporter()

# Analyze and export
analysis = client.analyze_contract("0x...", "ethereum")
exporter.export_to_json(analysis, "usdc_analysis.json")

# Auto-generated filename with timestamp
exporter.export_to_json(analysis)  # Creates: contract_0x..._20240315_143022.json
```

**JSON Output:**
```json
{
  "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "name": "USD Coin",
  "symbol": "USDC",
  "chain": "ethereum",
  "security_score": 95,
  "risk_level": "low",
  "vulnerabilities": [],
  "is_verified": true,
  "key_functions": ["transfer", "approve", "mint"],
  "ai_insights": "..."
}
```

### 2. Markdown Export (Beautiful Reports)

Perfect for: Documentation, GitHub, technical writeups, stakeholder reports

```python
# Export as formatted Markdown
exporter.export_to_markdown(analysis, "usdc_report.md")
```

**Markdown Output:**

```markdown
# Contract Analysis Report: USD Coin

**Address:** `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`  
**Chain:** Ethereum  
**Security Score:** 95/100 🟢  
**Risk Level:** LOW  
**Generated:** 2024-03-15 14:30:22

---

## 📋 Summary

USDC is a fully-backed stablecoin issued by Circle...

## 🔑 Key Functions

| Function | Description |
|----------|-------------|
| transfer | Transfer tokens between addresses |
| approve  | Approve spending allowance |
| mint     | Create new tokens (admin only) |

## 🔒 Security Analysis

**Overall Score:** 95/100

✅ **Strengths:**
- Contract verified on Etherscan
- Proper access control
- No critical vulnerabilities

⚠️ **Considerations:**
- Centralized admin control
- Blacklist functionality

## 📊 Token Information

- **Symbol:** USDC
- **Decimals:** 6
- **Total Supply:** 51.68B USDC
```

### 3. CSV Export (Spreadsheet-Friendly)

Perfect for: Excel analysis, data visualization, quick reviews

```python
# Export as CSV (flattened key-value pairs)
exporter.export_to_csv(analysis, "usdc_data.csv")
```

**CSV Output:**
```csv
key,value
address,0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
name,USD Coin
symbol,USDC
chain,ethereum
security_score,95
risk_level,low
is_verified,true
key_functions_0,transfer
key_functions_1,approve
key_functions_2,mint
```

### Export Options

```python
from chainxplain.export import ReportExporter

exporter = ReportExporter()

# Works with all analysis types
contract_analysis = client.analyze_contract("0x...", "ethereum")
wallet_analysis = client.analyze_wallet("0x...", "ethereum")
tx_analysis = client.analyze_transaction("0x...", "ethereum")

# Export to all formats
exporter.export_to_json(contract_analysis, "contract.json")
exporter.export_to_markdown(contract_analysis, "contract.md")
exporter.export_to_csv(contract_analysis, "contract.csv")

# Auto-naming with timestamps
exporter.export_to_json(wallet_analysis)  # wallet_0x..._20240315_143022.json
exporter.export_to_markdown(tx_analysis)  # transaction_0x..._20240315_143022.md
```

### Report Directory

All exports are saved to `./reports/` by default (auto-created):

```
reports/
├── contract_0xA0b8...eB48_20240315_143022.json
├── contract_0xA0b8...eB48_20240315_143022.md
├── wallet_0xd8dA...bEb0_20240315_150000.json
└── transaction_0x1234...abcd_20240315_160000.csv
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
CACHE_TTL=3600                 # Cache duration in seconds (not yet implemented)
RATE_LIMIT=5                   # AI API calls per minute (enforced automatically)
MAX_TOKENS=4096                # Max AI response tokens
DEFAULT_CHAIN=ethereum         # Default blockchain
```

### Configuration via Python

```python
from chainxplain import ChainXplain, ChainConfig

# Override environment variables
client = ChainXplain(
    ai_provider="openai",
    openai_api_key="sk-...",
    alchemy_api_key="...",
    etherscan_api_key="...",
    chain=ChainConfig.ETHEREUM
)

# Switch chains dynamically
client.chain = ChainConfig.POLYGON
analysis = client.analyze_contract("0x...", "polygon")

client.chain = ChainConfig.ARBITRUM
wallet = client.analyze_wallet("0x...", "arbitrum")
```

### Rate Limiting

ChainXplain automatically enforces **5 AI API calls per minute** to prevent quota exhaustion:

```python
# Rate limiting is transparent - requests are automatically delayed
for address in contract_addresses:
    analysis = client.analyze_contract(address, "ethereum")
    # If 5 calls already made this minute, automatically sleeps until next minute
    print(f"Analyzed: {analysis.name}")
```

### Input Validation

All user inputs are automatically validated:

```python
from chainxplain.validation import (
    validate_ethereum_address,
    validate_transaction_hash,
    validate_chain_name,
    ValidationError
)

# Manual validation (automatic in ChainXplain methods)
try:
    validate_ethereum_address("0xInvalidAddress")
except ValidationError as e:
    print(f"Error: {e}")  # "Invalid Ethereum address format"

# Chain validation
validate_chain_name("ethereum")  # ✅ Valid
validate_chain_name("solana")    # ❌ ValidationError: Unsupported chain

# Transaction hash validation
validate_transaction_hash("0x" + "a" * 64)  # ✅ Valid (66 chars)
validate_transaction_hash("0x123")          # ❌ ValidationError: Invalid format
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
┌──────────────────────────────────────────────────────────────────┐
│                        ChainXplain                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  CLI Tool        Python Library      REST API        MCP Server  │
│  ├─ Typer       ├─ ChainXplain()    ├─ FastAPI     ├─ FastMCP  │
│  ├─ Rich UI     ├─ analyze_*()      ├─ 9 Endpoints ├─ 5 Tools  │
│  └─ Commands    └─ ReportExporter   ├─ CORS        └─ Claude   │
│                                     └─ Auto Docs                │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                      Core Components                              │
│  ├─ AI Analyzer (ChatGPT/Claude) - Natural language insights    │
│  ├─ Security Analyzer - 9 vulnerability patterns                │
│  ├─ Input Validator - SQL injection & XSS prevention            │
│  ├─ Blockchain Clients (Web3, Alchemy)                          │
│  ├─ Explorer Integration (Etherscan APIs)                       │
│  ├─ Export Engine (JSON, CSV, Markdown)                         │
│  └─ Rate Limiter (5 AI calls/min automatic)                     │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                    External Services                              │
│  ├─ OpenAI/Anthropic (AI Analysis)                              │
│  ├─ Alchemy (Enhanced Blockchain APIs)                          │
│  ├─ Etherscan (Contract Verification)                           │
│  └─ Public RPCs (Fallback)                                      │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Request → Input Validation → Blockchain Data Fetch → Security Scan
    ↓                ↓                      ↓                    ↓
  CLI/API      ValidationError       Web3/Alchemy        SecurityAnalyzer
                                            ↓                    ↓
                                    AI Analysis (Rate Limited) ←─┘
                                            ↓
                                    Pydantic Models
                                            ↓
                                    Export (JSON/CSV/MD)
                                            ↓
                                    Return to User
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

**Quick Start for Contributors:**

```bash
# Fork and clone
git clone https://github.com/your-username/chainxplain.git
cd chainxplain

# Setup development environment
poetry install --with dev
poetry run pre-commit install

# Make changes and test
poetry run pytest --cov=src/chainxplain
poetry run ruff check src/ tests/
poetry run ruff format src/ tests/
poetry run mypy src/

# Submit PR
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
```

**What to Contribute:**
- 🐛 Bug fixes
- ✨ New features (security patterns, chain support, export formats)
- 📝 Documentation improvements
- 🧪 Additional test coverage
- 🎨 UI/UX enhancements

**Before Submitting:**
- ✅ All tests pass (`pytest`)
- ✅ Code formatted (`ruff format`)
- ✅ No linting errors (`ruff check`)
- ✅ Type checking passes (`mypy`)
- ✅ Added tests for new features
- ✅ Updated documentation

---

## 📦 Publishing to PyPI

**For Maintainers:**

```bash
# Update version in pyproject.toml
poetry version patch  # or minor, major

# Build package
poetry build

# Publish to PyPI (requires PyPI token)
poetry publish

# Create GitHub release
git tag v0.1.1
git push origin v0.1.1
```

**Setup Required:**
1. **PyPI Account** - Register at https://pypi.org/
2. **PyPI Token** - Generate at https://pypi.org/manage/account/token/
3. **Codecov Token** - Add to GitHub Secrets for coverage reporting
4. Configure Poetry: `poetry config pypi-token.pypi your-token-here`

Once published, the PyPI badges will automatically work:
- [![PyPI version](https://badge.fury.io/py/chainxplain.svg)](https://badge.fury.io/py/chainxplain) (future)
- [![Downloads](https://pepy.tech/badge/chainxplain)](https://pepy.tech/project/chainxplain) (future)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Bharath Preetham

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-4o for intelligent analysis
- **Anthropic** - Claude 3.5 Sonnet AI
- **Alchemy** - Enhanced blockchain APIs
- **Etherscan** - Blockchain explorer data
- **FastMCP** - Modern MCP implementation

---

## 🌟 Features at a Glance

✅ **Multi-Chain Support** - Ethereum, Polygon, Arbitrum, Optimism, Base, BSC  
✅ **Dual AI Providers** - ChatGPT (GPT-4o) & Claude (3.5 Sonnet)  
✅ **Smart Contract Analysis** - Decode, explain, risk assessment  
✅ **Advanced Security Scanning** - 9+ vulnerability patterns, 0-100 scoring  
✅ **Wallet Insights** - Holdings, balance, transaction patterns  
✅ **Transaction Decoding** - Function calls, parameters, event logs  
✅ **Export Reports** - JSON, CSV, Markdown formats  
✅ **REST API Server** - FastAPI with 9 endpoints, auto-docs  
✅ **Input Validation** - SQL injection & XSS prevention  
✅ **Rate Limiting** - Automatic 5 AI calls/min enforcement  
✅ **MCP Server** - Claude Desktop & AI agent integration  
✅ **CLI & Python Library** - Multiple integration options  
✅ **Production Ready** - Logging, error handling, type safety  
✅ **Comprehensive Testing** - 24 tests, 39% coverage  

---

## 🎓 Learn More

- **[Installation Guide](#-quick-start)** - Get up and running in 5 minutes
- **[CLI Examples](#-usage-examples)** - Command-line usage patterns
- **[Python Library Guide](#-python-library-usage)** - Integrate into your code
- **[REST API Docs](#-rest-api-server)** - HTTP endpoint reference
- **[Security Features](#-security-features)** - Vulnerability detection guide
- **[Export Guide](#-export--reporting)** - Generate reports
- **[Configuration Reference](#%EF%B8%8F-configuration-reference)** - Environment variables
- **[Architecture Overview](#-architecture)** - System design

---

**Made with ❤️ for the blockchain community**