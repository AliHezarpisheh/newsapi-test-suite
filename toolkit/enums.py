"""Module providing enumeration classes for response statuses and codes."""

from enum import Enum


class ResponseStatusEnum(str, Enum):
    """Enumeration of possible response statuses."""

    OK = "ok"
    ERROR = "error"


class ResponseCodeEnum(str, Enum):
    """Enumeration of possible response codes."""

    API_KEY_MISSING = "apiKeyMissing"
    API_KEY_INVALID = "apiKeyInvalid"
    PARAMETER_INVALID = "parameterInvalid"
    PARAMETER_MISSING = "parametersMissing"
    SOURCES_DOES_NOT_EXIST = "sourceDoesNotExist"
    PAGE_CAN_NOT_BE_LESS_THAN_ONE = "pageCannotBeLessThanOne"
    Maximum_RESULTS_REACHED = "maximumResultsReached"
    RATE_LIMITED = "rateLimited"


class APIEndpointEnum(str, Enum):
    """Enumeration of the API endpoints."""

    EVERYTHING = "/everything"
    TOP_HEADLINES = "/top_headlines"
    SOURCES = "/sources"
