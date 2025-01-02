"""Module for handling settings in the application."""

from functools import lru_cache
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Class for handling all the settings in the application."""

    # API Settings
    BASE_URL: Annotated[
        str, Field(description="The base url for the API getting tested")
    ]
    API_KEY: Annotated[str, Field(description="The API key, used for auth")]
    RATE_LIMITED_API_KEY: Annotated[
        str, Field(description="The API key which is rate limited")
    ]

    # Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        use_enum_values=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the instance of `Settings`, using lru_caching."""
    return Settings()
