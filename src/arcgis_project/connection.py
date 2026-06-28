"""Authenticate a :class:`~arcgis.gis.GIS` connection from :class:`Settings`.

The ``arcgis`` package is an *optional* dependency, so it is imported lazily
inside :func:`connect`. That keeps the rest of the package (and the test suite)
usable without the heavy geospatial stack installed.
"""

from __future__ import annotations

from typing import Any

from .config import Settings


def _import_gis():
    try:
        from arcgis.gis import GIS  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised only without arcgis
        raise ImportError(
            "The 'arcgis' package is required for live portal access. "
            "Install it with:  pip install -e \".[arcgis]\""
        ) from exc
    return GIS


def gis_kwargs(settings: Settings) -> dict:
    """Translate :class:`Settings` into keyword args for ``GIS(...)``.

    Exposed separately so the mapping can be unit-tested without constructing a
    real connection.
    """
    method = settings.auth_method
    if method == "api_key":
        return {"url": settings.url, "api_key": settings.api_key}
    if method == "userpass":
        return {
            "url": settings.url,
            "username": settings.username,
            "password": settings.password,
        }
    if method == "profile":
        return {"url": settings.url, "profile": settings.profile}
    # anonymous
    return {"url": settings.url}


def connect(settings: Settings | None = None) -> Any:
    """Create and return an authenticated ``GIS`` object.

    :param settings: connection settings; defaults to ``Settings.from_env()``.
    """
    settings = settings or Settings.from_env()
    GIS = _import_gis()
    return GIS(**gis_kwargs(settings))
