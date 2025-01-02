"""Module containing test cases for authentication-related functionality."""

from http import HTTPStatus

import pytest

from config.base import settings
from toolkit import (
    APIEndpointEnum,
    AsyncAPIClient,
    ResponseCodeEnum,
    ResponseStatusEnum,
)


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_valid_api_key_in_x_api_key_header_success(
    api_client: AsyncAPIClient,
) -> None:
    """Test successful response with valid API key in X-API-KEY header."""
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params={"q": "bitcoin"}
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert articles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token_type",
    [
        "",
        "Bearer ",
    ],
)
async def test_valid_api_key_in_authorization_header_success(token_type: str) -> None:
    """Test successful response with valid API key in Authorization header."""
    api_client = AsyncAPIClient(
        base_url=settings.BASE_URL,
        default_headers={"Authorization": token_type + settings.API_KEY},
    )

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin"},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert articles


@pytest.mark.asyncio
async def test_valid_api_key_in_query_param_success() -> None:
    """Test successful response with valid API key in query parameter."""
    api_client = AsyncAPIClient(base_url=settings.BASE_URL)

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin", "apiKey": settings.API_KEY},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert articles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "header_name",
    [
        "X-API-KEY",
        "Authorization",
    ],
)
async def test_valid_api_keys_in_param_and_header_success(header_name: str) -> None:
    """Test successful response with valid API key in both query param and header."""
    api_client = AsyncAPIClient(
        base_url=settings.BASE_URL, default_headers={header_name: settings.API_KEY}
    )

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin", "apiKey": settings.API_KEY},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert articles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "header_name",
    [
        "X-API-KEY",
        "Authorization",
    ],
)
async def test_valid_api_key_in_query_param_despite_invalid_key_in_header_success(
    header_name: str,
) -> None:
    """Test success response with valid key in query param despite invalid header."""
    invalid_api_key = "invalid_api_key"
    api_client = AsyncAPIClient(
        base_url=settings.BASE_URL, default_headers={header_name: invalid_api_key}
    )

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin", "apiKey": settings.API_KEY},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert articles


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize(
    "invalid_api_key",
    [
        "invalid_key",
        "",
        None,
        "a" * 1000,
    ],
)
async def test_invalid_api_key_in_x_api_key_header_failure(
    invalid_api_key: str,
) -> None:
    """Test failure response with invalid API key in X-API-KEY header."""
    api_client = AsyncAPIClient(
        base_url=settings.BASE_URL,
        default_headers={"X-API-KEY": invalid_api_key},
    )

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin"},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UNAUTHORIZED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.API_KEY_INVALID.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your API key is invalid or incorrect. Check your key, or go to "
        "https://newsapi.org to create a free API key."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize(
    "token_type",
    [
        "",
        "Bearer ",
    ],
)
@pytest.mark.parametrize(
    "invalid_api_key",
    [
        "invalid_key",
        "",
        None,
        "a" * 1000,
    ],
)
async def test_invalid_api_key_in_authorization_header_failure(
    token_type: str, invalid_api_key: str
) -> None:
    """Test failure response with invalid API key in Authorization header."""
    api_client = AsyncAPIClient(
        base_url=settings.BASE_URL,
        default_headers={"Authorization": token_type + invalid_api_key},
    )

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin"},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UNAUTHORIZED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.API_KEY_INVALID.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your API key is invalid or incorrect. Check your key, or go to "
        "https://newsapi.org to create a free API key."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize(
    "invalid_api_key",
    [
        "invalid_key",
        "",
        None,
        "a" * 1000,
    ],
)
async def test_invalid_api_key_in_query_param_failure(invalid_api_key: str) -> None:
    """Test failure response with invalid API key in query parameter."""
    api_client = AsyncAPIClient(base_url=settings.BASE_URL)

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin", "apiKey": invalid_api_key},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UNAUTHORIZED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.API_KEY_INVALID.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your API key is invalid or incorrect. Check your key, or go to "
        "https://newsapi.org to create a free API key."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "header_name",
    [
        "X-API-KEY",
        "Authorization",
    ],
)
async def test_invalid_api_key_in_query_param_despite_valid_key_in_header_failure(
    header_name: str,
) -> None:
    """Test failure response invalid API key in q param despite valid header key."""
    api_client = AsyncAPIClient(
        base_url=settings.BASE_URL, default_headers={header_name: settings.API_KEY}
    )

    invalid_api_key = "invalid_api_key"
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin", "apiKey": invalid_api_key},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UNAUTHORIZED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.API_KEY_INVALID.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your API key is invalid or incorrect. Check your key, or go to "
        "https://newsapi.org to create a free API key."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
async def test_missing_api_key_failure() -> None:
    """Test failure response when API key is missing."""
    api_client = AsyncAPIClient(base_url=settings.BASE_URL)

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin"},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UNAUTHORIZED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.API_KEY_MISSING.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your API key is missing. Append this to the URL with the apiKey param, or use "
        "the x-api-key HTTP header."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
async def test_rate_limited_api_key_failure() -> None:
    """Test failure response when API key is rate-limited."""
    api_client = AsyncAPIClient(base_url=settings.BASE_URL)

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": "bitcoin", "apiKey": settings.RATE_LIMITED_API_KEY},
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.TOO_MANY_REQUESTS
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.RATE_LIMITED.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "You have made too many requests recently. Developer accounts are limited to "
        "100 requests over a 24 hour period (50 requests available every 12 hours). "
        "Please upgrade to a paid plan if you need more requests."
    )
    assert actual_response_message == expected_response_message
