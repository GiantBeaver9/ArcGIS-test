"""Exceptions raised by the REST client."""

from __future__ import annotations

from typing import Optional


class ArcGISRestError(RuntimeError):
    """Raised when the ArcGIS REST API returns an error payload.

    The ArcGIS REST API returns HTTP 200 even for logical errors, embedding an
    ``{"error": {...}}`` object in the body. This exception surfaces that.
    """

    def __init__(self, message: str, *, code: Optional[int] = None, details=None):
        super().__init__(message)
        self.code = code
        self.details = details or []
