# Contributing to ChainXplain

Thank you for your interest in contributing to ChainXplain! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Git for version control

### Setup Development Environment

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/chainxplain.git
cd chainxplain
```

2. **Install dependencies**

```bash
poetry install --with dev
```

3. **Set up pre-commit hooks**

```bash
poetry run pre-commit install
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run tests to verify setup**

```bash
poetry run pytest
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

Follow our coding standards:

- **Code Style**: We use `ruff` for linting and `black` for formatting
- **Type Hints**: All functions should have type hints
- **Docstrings**: Use Google-style docstrings
- **Tests**: Write tests for new features

### 3. Run Quality Checks

```bash
# Format code
poetry run black src/ tests/

# Lint code
poetry run ruff check src/ tests/

# Type check
poetry run mypy src/

# Run tests
poetry run pytest

# Run all checks (recommended before committing)
poetry run pre-commit run --all-files
```

### 4. Commit Your Changes

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add support for new blockchain"
git commit -m "fix: resolve rate limiting issue"
git commit -m "docs: update API documentation"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### 5. Push and Create Pull Request

```bash
git push origin feat/your-feature-name
```

Then create a PR on GitHub with:
- Clear title following conventional commits
- Description of changes
- Reference to related issues
- Screenshots/examples if applicable

## 🧪 Testing Guidelines

### Writing Tests

```python
# tests/test_example.py
import pytest
from chainxplain import ChainExplainClient

def test_client_initialization():
    """Test that client initializes correctly."""
    client = ChainExplainClient(
        anthropic_api_key="test-key",
        etherscan_api_key="test-key"
    )
    assert client is not None

@pytest.mark.asyncio
async def test_async_functionality():
    """Test async functionality."""
    # Your async test here
    pass
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_client.py

# Run with coverage
poetry run pytest --cov=chainxplain --cov-report=html

# Run integration tests (requires API keys)
poetry run pytest tests/integration/
```

## 📚 Documentation

### Docstring Format

We use Google-style docstrings:

```python
def analyze_contract(
    address: str,
    chain: str = "ethereum"
) -> ContractAnalysis:
    """
    Analyze a smart contract.
    
    Args:
        address: Contract address (0x-prefixed hex string)
        chain: Blockchain network name (default: "ethereum")
        
    Returns:
        ContractAnalysis object with detailed analysis
        
    Raises:
        ValueError: If address format is invalid
        APIError: If API request fails
        
    Example:
        >>> result = analyze_contract("0x123...", "ethereum")
        >>> print(result.summary)
    """
    pass
```

### Building Documentation

```bash
# Install docs dependencies
poetry install --with dev

# Build docs
poetry run mkdocs build

# Serve docs locally
poetry run mkdocs serve
```

## 🔍 Code Review Process

### What We Look For

1. **Code Quality**
   - Follows style guidelines
   - Has type hints
   - Includes docstrings
   - No unnecessary complexity

2. **Testing**
   - New features have tests
   - Tests pass in CI
   - Good test coverage

3. **Documentation**
   - README updated if needed
   - CHANGELOG updated
   - Docstrings are clear

4. **Commits**
   - Follow conventional commits
   - Atomic and logical commits
   - Clear commit messages

### PR Requirements

- [ ] All tests pass
- [ ] Code is formatted and linted
- [ ] Type checks pass
- [ ] Documentation updated
- [ ] CHANGELOG updated (for significant changes)
- [ ] No merge conflicts

## 🐛 Reporting Bugs

Create an issue with:

1. **Clear title** describing the bug
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (Python version, OS, etc.)
6. **Code snippet** if applicable

## 💡 Suggesting Features

Create an issue with:

1. **Clear description** of the feature
2. **Use case** explaining why it's needed
3. **Proposed implementation** (if you have ideas)
4. **Alternative solutions** you've considered

## 📋 Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create and push tag:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```
4. GitHub Actions will automatically:
   - Run all tests
   - Build packages
   - Publish to PyPI
   - Create GitHub release
   - Build and push Docker image

## 🎯 Project Structure

```
chainxplain/
├── src/chainxplain/       # Main package
│   ├── ai/                # AI analysis
│   ├── blockchain/        # Blockchain integrations
│   ├── cli/               # CLI tool
│   ├── mcp/               # MCP server
│   ├── client.py          # Main client
│   ├── config.py          # Configuration
│   └── models.py          # Data models
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── performance/       # Performance tests
├── examples/              # Example scripts
├── docs/                  # Documentation
└── .github/               # GitHub Actions workflows
```

## 💬 Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **Discord**: [Join our community](#) (if available)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Thank you for contributing to ChainXplain! Every contribution helps make blockchain data more accessible and understandable.
