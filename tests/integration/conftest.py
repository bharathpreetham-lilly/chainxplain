"""Integration tests requiring real API keys.

These tests are skipped by default and only run when API keys are available.
Run with: pytest tests/integration/ --run-integration
"""

import pytest
import os


def pytest_addoption(parser):
    """Add custom pytest option for integration tests."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests that require API keys",
    )


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring API keys"
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --run-integration is passed."""
    if config.getoption("--run-integration"):
        return
    
    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@pytest.fixture(scope="session")
def has_api_keys():
    """Check if required API keys are available."""
    return bool(
        os.getenv("ANTHROPIC_API_KEY") and
        os.getenv("ETHERSCAN_API_KEY")
    )


@pytest.fixture(scope="session")
def skip_if_no_keys(has_api_keys):
    """Skip test if API keys are not available."""
    if not has_api_keys:
        pytest.skip("API keys not available")
