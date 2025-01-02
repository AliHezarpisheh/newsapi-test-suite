"""Module containing test cases for the `/top-headlines/sources` endpoint."""

import random
from http import HTTPStatus
from typing import Any

import pytest

from toolkit import APIEndpointEnum, AsyncAPIClient, ResponseStatusEnum


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_valid_simple_request_to_sources_endpoint_success(
    api_client: AsyncAPIClient,
) -> None:
    """Test successful response for a simple request to the '/top-headlines/sources'."""
    response = await api_client.get(APIEndpointEnum.SOURCES.value)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `articles` in body")
    assert news_sources

    # Check the fields in the sources
    random_index = random.randint(0, 99)
    random_article: dict[str, Any] = news_sources[random_index]
    actual_keys = set(random_article.keys())
    expected_keys = {
        "id",
        "name",
        "description",
        "url",
        "category",
        "language",
        "country",
    }
    assert actual_keys == expected_keys


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "category",
    [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
        "all",
    ],
)
async def test_valid_category_query_param_success(
    api_client: AsyncAPIClient, category: str
) -> None:
    """Test successful response with category query parameter."""
    query_param = {"category": category}
    response = await api_client.get(APIEndpointEnum.SOURCES.value, params=query_param)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `sources` in body")
    random_index = random.randint(5, 20)
    for news_source in news_sources[:random_index]:
        actual_category = news_source.get("category", "No `category` in body")
        expected_category = category
        assert actual_category == expected_category


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language",
    [
        "ar",
        "de",
        "en",
        "es",
        "fr",
        "he",
        "it",
        "nl",
        "no",
        "pt",
        "ru",
        "sv",
        "ud",
        "zh",
        "all",
    ],
)
async def test_valid_language_query_param_success(
    api_client: AsyncAPIClient, language: str
) -> None:
    """Test successful response with language query parameter."""
    query_param = {"language": language}
    response = await api_client.get(APIEndpointEnum.SOURCES.value, params=query_param)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `sources` in body")
    random_index = random.randint(5, 20)
    for news_source in news_sources[:random_index]:
        actual_language = news_source.get("language", "No `language` in body")
        expected_language = language
        assert actual_language == expected_language


# Didn't include all countries due to rate limiting issues (In dev mode)
@pytest.mark.asyncio
@pytest.mark.parametrize("country", ["ae", "ar", "at", "au", "be", "bg", "br", "all"])
async def test_valid_country_query_param_success(
    api_client: AsyncAPIClient, country: str
) -> None:
    """Test successful response with country query parameter."""
    query_param = {"country": country}
    response = await api_client.get(APIEndpointEnum.SOURCES.value, params=query_param)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `sources` in body")
    random_index = random.randint(5, 20)
    for news_source in news_sources[:random_index]:
        actual_country = news_source.get("country", "No `country` in body")
        expected_country = country
        assert actual_country == expected_country


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "category",
    [
        "invalid_category",
        "BUSINESS",
        "123",
        "!@#$%",
        "",
        None,
    ],
)
async def test_invalid_category_query_param_should_not_affect_response_success(
    api_client: AsyncAPIClient, category: str
) -> None:
    """Test successful response with invalid category query param."""
    query_param = {"category": category}
    response = await api_client.get(APIEndpointEnum.SOURCES.value, params=query_param)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `sources` in body")
    assert news_sources and isinstance(news_sources, list)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language",
    [
        "invalid_language",
        "EN",
        "123",
        "!@#$%",
        "",
        None,
    ],
)
async def test_invalid_language_query_param_should_not_affect_response_success(
    api_client: AsyncAPIClient, language: str
) -> None:
    """Test successful response with invalid language query param."""
    query_param = {"language": language}
    response = await api_client.get(APIEndpointEnum.SOURCES.value, params=query_param)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `sources` in body")
    assert news_sources and isinstance(news_sources, list)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "country",
    [
        "invalid_country",
        "US",
        "123",
        "!@#$%",
        "",
        None,
    ],
)
async def test_invalid_country_query_param_should_not_affect_response_success(
    api_client: AsyncAPIClient, country: str
) -> None:
    """Test successful response with invalid country query param."""
    query_param = {"country": country}
    response = await api_client.get(APIEndpointEnum.SOURCES.value, params=query_param)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    news_sources = response.json().get("sources", "No `sources` in body")
    assert news_sources and isinstance(news_sources, list)
