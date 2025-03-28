import pytest

def pytest_configure(config):
    """Configure pytest."""
    # Register marks for asyncio tests
    config.addinivalue_line("markers", "asyncio: mark test as an asyncio test")

