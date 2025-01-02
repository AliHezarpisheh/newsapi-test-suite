"""Module containing behavioral tests for the `/top-headlines` endpoint."""

import random
from http import HTTPStatus
from typing import Any

import httpx
from pytest_bdd import given, scenarios, then, when

from config.base import settings
from toolkit.api_clients import APIClient
from toolkit.enums import APIEndpointEnum, ResponseStatusEnum

scenarios("../features/scenarios.feature")


@given(
    "a user with a valid API key",
    target_fixture="response",
)
def given_user_with_valid_api_key() -> httpx.Response:
    """
    Provide a user with a valid API key for making API requests.

    Returns
    -------
    httpx.Response
        An instance of httpx.Response indicating the HTTP response.
    """
    api_client = APIClient(
        base_url=settings.BASE_URL,
        default_headers={"X-API-KEY": settings.API_KEY},
    )
    query_params = {"country": "us"}
    response = api_client.get(APIEndpointEnum.TOP_HEADLINES.value, params=query_params)
    return response


@when('I send a GET request to "/v2/top-headlines"')
def when_get_request_made() -> None:
    """
    Send a GET request to the `/v2/top-headlines` endpoint.

    This step does not return any value as it serves as a trigger for the test. The
    when step in `pytest-bdd` can not create fixtures, so the given step should actually
    call the API.
    """


@then("the response status code should be 200")
def then_response_status_code_should_be_200(response: httpx.Response) -> None:
    """
    Validate that the response status code is 200.

    Parameters
    ----------
    response : httpx.Response
        The HTTP response object returned by the API.

    Raises
    ------
    AssertionError
        If the response status code does not match the expected value.
    """
    actual_response_status_code = response.status_code
    expected_response_status_code = HTTPStatus.OK
    assert actual_response_status_code == expected_response_status_code


@then("the response should be valid")
def then_response_should_be_valid(response: httpx.Response) -> None:
    """
    Validate response structure and data integrity for the `/top-headlines` endpoint.

    Parameters
    ----------
    response : httpx.Response
        The HTTP response object returned by the API.

    Raises
    ------
    AssertionError
        If the response structure or data does not match the expected format.
    """
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
