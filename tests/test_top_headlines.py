"""Module containing test cases for the `/top-headlines` endpoint."""

import random
from http import HTTPStatus
from typing import Any

import pytest

from toolkit import APIEndpointEnum, AsyncAPIClient, ResponseStatusEnum


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_valid_simple_request_to_top_headlines_endpoint_success(
    api_client: AsyncAPIClient,
) -> None:
    """Test successful response for a simple request to the 'top-headlines' endpoint."""
    query_params = {"country": "us"}

    response = await api_client.get(
        APIEndpointEnum.TOP_HEADLINES.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    total_results = response.json().get("totalResults", "No `totalResults` in body")
    assert total_results >= 0

    articles = response.json().get("articles", "No `articles` in body")
    assert articles

    # The default pageSize param is 100. So it should be 100 articles in the body
    actual_len_articles = len(articles)
    expected_len_articles = 20
    assert actual_len_articles == expected_len_articles

    # Check the fields in the articles
    random_index = random.randint(0, 19)
    random_article: dict[str, Any] = articles[random_index]
    actual_keys = set(random_article.keys())
    expected_keys = {
        "source",
        "author",
        "title",
        "description",
        "url",
        "urlToImage",
        "publishedAt",
        "content",
    }
    assert actual_keys == expected_keys

    # Check the source fields
    random_index = random.randint(0, 19)
    random_source: dict[str, Any] = articles[random_index].get("source")
    actual_source_keys = set(random_source.keys())
    expected_source_keys = {"id", "name"}
    assert actual_source_keys == expected_source_keys
