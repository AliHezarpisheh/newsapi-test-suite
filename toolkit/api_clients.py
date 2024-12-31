"""Client for making HTTP requests using the httpx library."""

from typing import Any

import httpx


class BaseAPIClient:
    """Parent class for API clients."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        default_headers: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the subclasses of the `BaseAPIClient`."""
        self.base_url = base_url
        self.timeout = timeout
        self.default_headers = default_headers or {}


class APIClient(BaseAPIClient):
    """`APIClient` class for making synchronous HTTP requests."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        default_headers: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the `APIClient`."""
        super().__init__(
            base_url=base_url, timeout=timeout, default_headers=default_headers
        )
        self._client = httpx.Client

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make a synchronous HTTP request.

        Parameters
        ----------
        method : str
            HTTP method (GET, POST, PUT, PATCH, DELETE).
        endpoint : str
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request payload for methods like POST, PUT, PATCH.
        **kwargs
            Additional keyword arguments for httpx.Client.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        request_headers = {**self.default_headers, **(headers or {})}

        with self._client() as client:
            response: httpx.Response = client.request(
                method,
                full_url,
                headers=request_headers,
                params=params,
                data=payload,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response

    def get(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make a synchronous HTTP GET request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        **kwargs
            Additional keyword arguments for httpx.Client.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = self._request(
            method="GET", endpoint=endpoint, headers=headers, params=params, **kwargs
        )
        return response

    def post(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make a synchronous HTTP POST request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request data.
        **kwargs
            Additional keyword arguments for httpx.Client.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = self._request(
            method="POST",
            endpoint=endpoint,
            headers=headers,
            params=params,
            payload=payload,
            **kwargs,
        )
        return response

    def put(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make a synchronous HTTP PUT request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request data.
        **kwargs
            Additional keyword arguments for httpx.Client.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = self._request(
            method="PUT",
            endpoint=endpoint,
            headers=headers,
            params=params,
            payload=payload,
            **kwargs,
        )
        return response

    def patch(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make a synchronous HTTP PATCH request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request data.
        **kwargs
            Additional keyword arguments for httpx.Client.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = self._request(
            method="PATCH",
            endpoint=endpoint,
            headers=headers,
            params=params,
            payload=payload,
            **kwargs,
        )
        return response

    def delete(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make a synchronous HTTP DELETE request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        **kwargs
            Additional keyword arguments for httpx.Client.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = self._request(
            method="DELETE", endpoint=endpoint, headers=headers, params=params, **kwargs
        )
        return response

    def __str__(self) -> str:
        """Return a human-readable string representation of the `APIClient`."""
        return f"APIClient - Base URL: {self.base_url}, Timeout: {self.timeout}s"

    def __repr__(self) -> str:
        """Return an unambiguous string representation of the `APIClient`."""
        return (
            f"APIClient(base_url={self.base_url}, "
            f"timeout={self.timeout}, "
            f"default_headers={self.default_headers})"
        )


class AsyncAPIClient(BaseAPIClient):
    """`AsyncAPIClient` class for making asynchronous HTTP requests."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        default_headers: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the `AsyncAPIClient`."""
        super().__init__(
            base_url=base_url, timeout=timeout, default_headers=default_headers
        )
        self._client = httpx.AsyncClient

    async def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP request.

        Parameters
        ----------
        method : str
            HTTP method (GET, POST, PUT, PATCH, DELETE).
        endpoint : str
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request payload for methods like POST, PUT, PATCH.
        **kwargs
            Additional keyword arguments for httpx.AsyncClient.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        request_headers = {**self.default_headers, **(headers or {})}

        async with self._client() as client:
            response: httpx.Response = await client.request(
                method,
                full_url,
                headers=request_headers,
                params=params,
                data=payload,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response

    async def get(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP GET request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        **kwargs
            Additional keyword arguments for httpx.AsyncClient.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = await self._request(
            method="GET", endpoint=endpoint, headers=headers, params=params, **kwargs
        )
        return response

    async def post(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP POST request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request data.
        **kwargs
            Additional keyword arguments for httpx.AsyncClient.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = await self._request(
            method="POST",
            endpoint=endpoint,
            headers=headers,
            params=params,
            payload=payload,
            **kwargs,
        )
        return response

    async def put(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP PUT request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request data.
        **kwargs
            Additional keyword arguments for httpx.AsyncClient.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = await self._request(
            method="PUT",
            endpoint=endpoint,
            headers=headers,
            params=params,
            payload=payload,
            **kwargs,
        )
        return response

    async def patch(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP PATCH request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        payload : dict, optional
            Request data.
        **kwargs
            Additional keyword arguments for httpx.AsyncClient.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = await self._request(
            method="PATCH",
            endpoint=endpoint,
            headers=headers,
            params=params,
            payload=payload,
            **kwargs,
        )
        return response

    async def delete(
        self,
        endpoint: str = "",
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP DELETE request.

        Parameters
        ----------
        endpoint : str, optional
            API endpoint.
        headers : dict, optional
            Additional headers for the request.
        params : dict, optional
            URL parameters.
        **kwargs
            Additional keyword arguments for httpx.AsyncClient.request.

        Returns
        -------
        httpx.Response
            The HTTP response object.
        """
        response = await self._request(
            method="DELETE", endpoint=endpoint, headers=headers, params=params, **kwargs
        )
        return response

    def __str__(self) -> str:
        """Return a human-readable string representation of the AsyncAPIClient."""
        return f"AsyncAPIClient - Base URL: {self.base_url}, Timeout: {self.timeout}s"

    def __repr__(self) -> str:
        """Return an unambiguous string representation of the AsyncAPIClient."""
        return (
            f"AsyncAPIClient(base_url={self.base_url}, "
            f"timeout={self.timeout}, "
            f"default_headers={self.default_headers})"
        )
