"""Configuration loaded from environment variables (and an optional .env file).

Keeping configuration in one place makes the rest of the package easy to test:
nothing else needs to read ``os.environ`` directly.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:  # python-dotenv is a light dependency; degrade gracefully if absent.
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is declared in dependencies
    def load_dotenv(*_args, **_kwargs):  # type: ignore[misc]
        return False


DEFAULT_URL = "https://www.arcgis.com"


@dataclass(frozen=True)
class Settings:
    """Resolved connection settings.

    Exactly one auth strategy is expected:

    * ``username`` + ``password``
    * ``api_key``
    * ``profile`` (a credential profile stored by the arcgis SDK keyring)

    If none are provided, an *anonymous* connection is implied (public content
    only).
    """

    url: str = DEFAULT_URL
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    profile: Optional[str] = None

    @classmethod
    def from_env(cls, *, load_env_file: bool = True) -> "Settings":
        """Build :class:`Settings` from environment variables.

        Reads ``ARCGIS_URL``, ``ARCGIS_USERNAME``, ``ARCGIS_PASSWORD``,
        ``ARCGIS_API_KEY`` and ``ARCGIS_PROFILE``. When ``load_env_file`` is
        true, a local ``.env`` file is loaded first (without overriding any
        variable already set in the real environment).
        """
        if load_env_file:
            load_dotenv(override=False)

        def _clean(name: str) -> Optional[str]:
            value = os.environ.get(name)
            value = value.strip() if value else value
            return value or None

        return cls(
            url=_clean("ARCGIS_URL") or DEFAULT_URL,
            username=_clean("ARCGIS_USERNAME"),
            password=_clean("ARCGIS_PASSWORD"),
            api_key=_clean("ARCGIS_API_KEY"),
            profile=_clean("ARCGIS_PROFILE"),
        )

    @property
    def auth_method(self) -> str:
        """Human-readable description of which auth strategy will be used."""
        if self.api_key:
            return "api_key"
        if self.username and self.password:
            return "userpass"
        if self.profile:
            return "profile"
        return "anonymous"

    def redacted(self) -> dict:
        """A dict safe to print/log — secrets are masked."""
        return {
            "url": self.url,
            "username": self.username,
            "password": _mask(self.password),
            "api_key": _mask(self.api_key),
            "profile": self.profile,
            "auth_method": self.auth_method,
        }


def _mask(secret: Optional[str]) -> Optional[str]:
    if not secret:
        return None
    if len(secret) <= 4:
        return "*" * len(secret)
    return secret[:2] + "*" * (len(secret) - 4) + secret[-2:]
