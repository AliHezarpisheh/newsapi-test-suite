"""Module providing pytest fixtures and configuration for the test suite."""

import pytest

from config.base import settings
from toolkit import AsyncAPIClient


@pytest.fixture(scope="session")
def api_client() -> AsyncAPIClient:
    """
    Fixture to provide an instance of AsyncAPIClient.

    This fixture sets up a client to interact with the API, initializing it with the
    base URL and API key from the settings. It is shared across all tests within the
    session.

    Returns
    -------
    AsyncAPIClient
        The API client instance for use in tests.
    """
    return AsyncAPIClient(
        base_url="https://newsapi.org/v2",
        default_headers={"X-API-KEY": settings.API_KEY},
    )
