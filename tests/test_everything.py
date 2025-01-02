"""Module containing test cases for the `/everything` endpoint."""

import random
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Any

import pytest

from toolkit import (
    APIEndpointEnum,
    AsyncAPIClient,
    ResponseCodeEnum,
    ResponseStatusEnum,
)


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_valid_simple_request_to_everything_endpoint_success(
    api_client: AsyncAPIClient,
) -> None:
    """Test successful response for a simple request to the 'everything' endpoint."""
    query_params = {"q": "tesla"}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
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
    expected_len_articles = 100
    assert actual_len_articles == expected_len_articles

    # Check the fields in the articles
    random_index = random.randint(0, 99)
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
    random_index = random.randint(0, 99)
    random_source: dict[str, Any] = articles[random_index].get("source")
    actual_source_keys = set(random_source.keys())
    expected_source_keys = {"id", "name"}
    assert actual_source_keys == expected_source_keys


async def test_valid_page_size_success(api_client: AsyncAPIClient) -> None:
    """Test successful response with a valid page size for the 'everything' endpoint."""
    random_page_size = random.randint(1, 100)
    query_params = {"q": "ai", "page": 1, "pageSize": random_page_size}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    actual_len_articles = len(articles)
    expected_len_articles = random_page_size
    assert actual_len_articles == expected_len_articles


# This test should be skipped because it could not be verified in dev mode
@pytest.mark.asyncio
@pytest.mark.skip
async def test_page_navigation_success(api_client: AsyncAPIClient) -> None:
    """Test successful page navigation through the 'everything' endpoint."""
    random_page_size = random.randint(1, 100)
    q = "attack+on+titan"
    query_params = {"q": q, "page": 1, "pageSize": random_page_size}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    articles = response.json().get("articles", "No `articles` in body")
    actual_len_articles = len(articles)
    expected_len_articles = random_page_size
    assert actual_len_articles == expected_len_articles

    # Check the last page
    total_results = response.json().get("totalResults", "No `totalResults` in body")
    last_page = total_results // random_page_size + (
        1 if total_results % random_page_size != 0 else 0
    )
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": q, "pageSize": random_page_size, "page": last_page},
    )
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    articles = response.json().get("articles", "No `articles` in body")
    assert articles

    # Check non-existing page
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value,
        params={"q": q, "pageSize": random_page_size, "page": last_page + 1},
    )
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    articles = response.json().get("articles", "No `articles` in body")
    assert not articles


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "q",
    [
        "bitcoin",
        '"exact phrase"',
        "+crypto",
        "-scam",
        "crypto AND (ethereum OR litecoin) NOT bitcoin",
        "blockchain technology",
        "crypto OR blockchain",
        "+finance +stocks -bonds",
        '"advanced search" AND (AI OR ML)',
    ],
)
async def test_valid_q_param_filters_success(
    api_client: AsyncAPIClient, q: str
) -> None:
    """Test successful response with valid query parameters, filtering results."""
    query_params = {"q": q, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
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
@pytest.mark.parametrize("sort_by", ["relevancy", "popularity", "publishedAt"])
async def test_valid_sort_by_success(api_client: AsyncAPIClient, sort_by: str) -> None:
    """Test success response for 'sortBy' parameters in 'everything' endpoint."""
    query_params = {"q": "pixies", "sortBy": sort_by, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)


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
    ],
)
async def test_valid_language_success(
    api_client: AsyncAPIClient, language: str
) -> None:
    """Test success response for different language params in 'everything' endpoint."""
    query_params = {"q": "radiohead", "language": language, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sources",
    [
        "abc-news",
        "die-zeit",
        "financial-post,handelsblatt",
    ],
)
async def test_valid_sources_success(api_client: AsyncAPIClient, sources: str) -> None:
    """Test success response for different source params in 'everything' endpoint."""
    query_params = {"q": "ethereum", "sources": sources, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)

    # TODO: Check the validity of the articles, filtered by the specified query params


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "domains",
    [
        "bbc.co.uk",
        "echcrunch.com",
        "engadget.com,bbc.co.uk",
    ],
)
async def test_valid_domains_success(api_client: AsyncAPIClient, domains: str) -> None:
    """Test success response for different domain params in 'everything' endpoint."""
    query_params = {"q": "ethereum", "domains": domains, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)

    # TODO: Check the validity of the articles, filtered by the specified query params


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exclude_domains",
    [
        "bbc.co.uk",
        "echcrunch.com",
        "engadget.com,bbc.co.uk",
    ],
)
async def test_valid_exclude_domains_success(
    api_client: AsyncAPIClient, exclude_domains: str
) -> None:
    """Test success response for different excludeDomains params."""
    query_params = {"q": "ethereum", "excludeDomains": exclude_domains, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)

    # TODO: Check the validity of the articles, filtered by the specified query params


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "from_param",
    [
        "2025-01-01",
        "2025-02-01T10:00:00",
        "2025-03-01T18:45:00",
    ],
)
async def test_valid_from_query_param_success(
    api_client: AsyncAPIClient, from_param: str
) -> None:
    """Test success response for valid 'from' query params in 'everything' endpoint."""
    query_params = {"q": "solidity", "from": from_param, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)

    from_datetime = datetime.fromisoformat(from_param).replace(tzinfo=timezone.utc)
    for article in articles:
        published_at = datetime.fromisoformat(
            article["publishedAt"].replace("Z", "+00:00")
        )
        assert published_at >= from_datetime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "to_param",
    [
        "2025-02-01",
        "2025-03-01T12:00:00",
        "2025-04-01T15:30:00",
    ],
)
async def test_valid_to_query_param_success(
    api_client: AsyncAPIClient, to_param: str
) -> None:
    """Test success response for various 'to' query params in 'everything' endpoint."""
    query_params = {"q": "solidity", "to": to_param, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)

    to_datetime = datetime.fromisoformat(to_param).replace(tzinfo=timezone.utc)
    for article in articles:
        published_at = datetime.fromisoformat(
            article["publishedAt"].replace("Z", "+00:00")
        )
        assert published_at <= to_datetime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "to_param",
    [
        "2025-02-01",
        "2025-03-01T12:00:00",
        "2025-04-01T15:30:00",
    ],
)
@pytest.mark.parametrize(
    "from_param",
    [
        "2025-01-01",
        "2025-02-01T10:00:00",
        "2025-03-01T18:45:00",
    ],
)
async def test_valid_to_and_from_query_param_success(
    api_client: AsyncAPIClient, to_param: str, from_param: str
) -> None:
    """Test success response for valid 'to' and 'from' query params in 'everything'."""
    query_params = {
        "q": "solidity",
        "to": to_param,
        "from": from_param,
        "pageSize": 5,
    }
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)

    from_datetime = datetime.fromisoformat(from_param).replace(tzinfo=timezone.utc)
    to_datetime = datetime.fromisoformat(to_param).replace(tzinfo=timezone.utc)
    for article in articles:
        published_at = datetime.fromisoformat(
            article["publishedAt"].replace("Z", "+00:00")
        )
        assert from_datetime <= published_at <= to_datetime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_in",
    [
        "title",
        "description",
        "content",
        "title,content",
        "title,description",
        "description,content",
        "content,title",
        "description,title",
        "content,description",
    ],
)
async def test_valid_search_in_success(
    api_client: AsyncAPIClient, search_in: str
) -> None:
    """Test successful response for valid 'searchIn' query params in 'everything'."""
    query_params = {"q": "silo", "searchIn": search_in, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)


@pytest.mark.asyncio
@pytest.mark.error
async def test_missing_any_param_failure(api_client: AsyncAPIClient) -> None:
    """Test failure when required parameters are missing in the request."""
    response = await api_client.get(APIEndpointEnum.EVERYTHING.value)

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.PARAMETER_MISSING.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Required parameters are missing, the scope of your search is too broad. "
        "Please set any of the following required parameters and try again: q, "
        "qInTitle, sources, domains."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize("page", [0, -1, -100])
async def test_invalid_page_number_failure(
    api_client: AsyncAPIClient, page: int
) -> None:
    """Test failure when an invalid page number is provided in the request."""
    page_size = 10
    query_params = {"q": "spain", "page": page, "pageSize": page_size}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.PAGE_CAN_NOT_BE_LESS_THAN_ONE.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        f"The page parameter cannot be less than 1. You have requested {page_size}."
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize("page", [None, "", "not-digits"])
async def test_invalid_page_value_failure(
    api_client: AsyncAPIClient, page: int
) -> None:
    """Test failure when an invalid page value (non-integer) is provided in request."""
    query_params = {"q": "spain", "page": page, "pageSize": 10}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.PAGE_CAN_NOT_BE_LESS_THAN_ONE.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "The request is invalid."  # TODO: This should be updated after back-end update
    )
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize("page_size", [-1, -100])
async def test_invalid_page_size_number_failure(
    api_client: AsyncAPIClient, page_size: int
) -> None:
    """Test failure when invalid pageSize (negative number) is provided in request."""
    query_params = {"q": "spain", "page": 1, "pageSize": page_size}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    # TODO: Add the `code` validation after back-end update

    actual_response_message = response.json().get("message", "No `message` in body")
    # TODO: This should be updated after back-end update
    expected_response_message = "The pageSize parameter cannot be less than 1."
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize("page_size", [None, "", "not-digits"])
async def test_invalid_page_size_value_failure(
    api_client: AsyncAPIClient, page_size: int
) -> None:
    """Test failure when invalid pageSize value (non-integer) is provided in request."""
    query_params = {"q": "spain", "page": 1, "pageSize": page_size}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    # TODO: Add the `code` validation after back-end update

    actual_response_message = response.json().get("message", "No `message` in body")
    # TODO: This should be updated after back-end update
    expected_response_message = "The request is invalid."
    assert actual_response_message == expected_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize("page_size", [101, 200, 1000000])
async def test_pagination_no_more_than_100_articles_per_page_failure(
    api_client: AsyncAPIClient, page_size: int
) -> None:
    """Test failure when more than 100 articles are requested per page in request."""
    query_params = {"q": "ai", "page": 1, "pageSize": page_size}

    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UPGRADE_REQUIRED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.MAXIMUM_RESULTS_REACHED.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = "You have requested too many results."
    assert expected_response_message in actual_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize(
    "q",
    [
        "crypto AND OR",
        "bitcoin AND",
        "NOT OR",
        "(crypto",
        "crypto)",
    ],
)
async def test_invalid_q_param_filters_failure(
    api_client: AsyncAPIClient, q: str
) -> None:
    """Test failure when invalid query parameters are provided in 'q' field."""
    query_params = {"q": q, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.QUERY_MALFORMED.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your query may be malformed - please check that all special "
        "chars (including &) in the query are URL escaped, and that it doesn't end "
        "with the OR or AND keyword."
    )
    assert expected_response_message in actual_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize(
    "q",
    [
        "",
        None,
        [],
        {},
    ],
)
async def test_invalid_nullable_q_param_filters_failure(
    api_client: AsyncAPIClient, q: str
) -> None:
    """Test failure when 'q' parameter is nullable."""
    query_params = {"q": q, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.PARAMETER_MISSING.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Required parameters are missing, the scope of your search is too broad. "
        "Please set any of the following required parameters and try again: q, "
        "qInTitle, sources, domains."
    )
    assert expected_response_message in actual_response_message


@pytest.mark.asyncio
@pytest.mark.error
async def test_invalid_long_q_param_filters_failure(
    api_client: AsyncAPIClient,
) -> None:
    """Test failure when 'q' parameter exceeds the maximum length."""
    query_params = {"q": "a" * 501, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.QUERY_TOO_LONG.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "Your query is too long (501 chars). Please reduce your query to 500 chars, "
        "or split it into multiple smaller requests."
    )
    assert expected_response_message in actual_response_message


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize("sort_by", ["invalid", "", None])
async def test_invalid_sort_by_should_not_affect_response_success(
    api_client: AsyncAPIClient, sort_by: str
) -> None:
    """Test that invalid 'sortBy' parameters do not affect the response."""
    query_params = {"q": "pixies", "sortBy": sort_by, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)


@pytest.mark.asyncio
@pytest.mark.error
@pytest.mark.parametrize(
    "language",
    [
        "",
        None,
        [],
        {},
    ],
)
async def test_nullable_language_should_not_affect_response_success(
    api_client: AsyncAPIClient, language: str
) -> None:
    """Test that nullable 'language' parameters do not affect the response."""
    query_params = {"q": "bitcoin", "language": language, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert len(articles) >= 0


@pytest.mark.asyncio
@pytest.mark.error
async def test_invalid_language_should_result_in_empty_list_success(
    api_client: AsyncAPIClient,
) -> None:
    """Test that invalid 'language' parameters result in an empty list of articles."""
    query_params = {"q": "radiohead", "language": "invalid", "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert len(articles) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exclude_domains",
    ["not-a-domain", "this-domain-does-not-exist.com", "", None, "bbc.co.uk,"],
)
async def test_invalid_exclude_domains_should_not_affect_response_success(
    api_client: AsyncAPIClient, exclude_domains: str
) -> None:
    """Test that invalid 'excludeDomains' parameters do not affect the response."""
    query_params = {"q": "ethereum", "excludeDomains": exclude_domains, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert isinstance(articles, list)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_in",
    [
        "invalid",
        "title,invalid",
        "invalid,invalid",
    ],
)
async def test_invalid_search_in_failure(
    api_client: AsyncAPIClient, search_in: str
) -> None:
    """Test failure when 'searchIn' parameter contains invalid values."""
    query_params = {"q": "silo", "searchIn": search_in, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.BAD_REQUEST
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.PARAMETER_INVALID.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = (
        "The valid options for the searchIn parameter are: title, description, "
        "content. You have entered 'invalid', which is not a valid field."
    )
    assert expected_response_message in actual_response_message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "from_param",
    [
        "invalid-date-format",
        "2025-13-01",
        "2025-02-30T10:00:00",
    ],
)
async def test_invalid_from_query_param_should_not_affect_response_success(
    api_client: AsyncAPIClient, from_param: str
) -> None:
    """Test that invalid 'from' query parameters do not affect the response."""
    query_params = {"q": "solidity", "from": from_param, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert len(articles) >= 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "to_param",
    [
        "2025-02-01T25:00:00",
        "2025-03-01T18:61:00",
        "2025-04-01T15:30:61",
    ],
)
async def test_invalid_to_query_param_should_not_affect_response_success(
    api_client: AsyncAPIClient, to_param: str
) -> None:
    """Test that invalid 'to' query parameters do not affect the response."""
    query_params = {"q": "solidity", "to": to_param, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert len(articles) >= 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "from_param, to_param",
    [
        ("2025-02-01T10:00:00", "2025-01-01T10:00:00"),
        ("2025-01-01T10:00:00", "2025-01-01T09:59:59"),
    ],
)
async def test_invalid_date_range_from_after_to_should_result_empty_list_success(
    api_client: AsyncAPIClient, from_param: str, to_param: str
) -> None:
    """Test that invalid date ranges where 'from' is after 'to' result in empty list."""
    query_params = {
        "q": "tesla",
        "from": from_param,
        "to": to_param,
        "pageSize": 5,
    }
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.OK.value
    assert actual_response_status == expected_response_status

    articles = response.json().get("articles", "No `articles` in body")
    assert len(articles) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "from_param",
    [
        (datetime.now(tz=timezone.utc) - timedelta(days=5 * 365 + 1)).isoformat(),
        (datetime.now(tz=timezone.utc) - timedelta(days=6 * 365)).isoformat(),
    ],
)
async def test_from_param_exceeds_5_years_failure(
    api_client: AsyncAPIClient, from_param: str
) -> None:
    """Test failure when 'from' query parameter is older than 5 years."""
    query_params = {"q": "solidity", "from": from_param, "pageSize": 5}
    response = await api_client.get(
        APIEndpointEnum.EVERYTHING.value, params=query_params
    )

    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.UPGRADE_REQUIRED
    assert actual_response_status_code == expected_response_status_code

    actual_response_status = response.json().get("status", "No `status` in body")
    expected_response_status = ResponseStatusEnum.ERROR.value
    assert actual_response_status == expected_response_status

    actual_response_code = response.json().get("code", "No `code` in body")
    expected_response_code = ResponseCodeEnum.PARAMETER_INVALID.value
    assert actual_response_code == expected_response_code

    actual_response_message = response.json().get("message", "No `message` in body")
    expected_response_message = "You are trying to request results too far in the past."
    assert expected_response_message in actual_response_message
