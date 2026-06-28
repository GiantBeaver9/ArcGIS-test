"""A minimal client for the ArcGIS REST API.

Design goals:

* **Thin** — no dependency on the full ``arcgis`` SDK.
* **Testable** — the HTTP transport is injectable, so the client can be
  exercised without network access (see the test suite).
* **Honest errors** — the ArcGIS REST API returns HTTP 200 with an embedded
  ``error`` object; we raise :class:`ArcGISRestError` for those.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .errors import ArcGISRestError

# A transport is any callable(method, url, params) -> parsed JSON dict.
Transport = Callable[[str, str, Dict[str, Any]], Dict[str, Any]]

DEFAULT_PORTAL = "https://www.arcgis.com"


def _requests_transport(timeout: float = 30.0) -> Transport:
    """Build the default transport backed by ``requests``.

    Imported lazily so importing this module never requires ``requests`` until
    an actual request is made with the default transport.
    """
    import requests  # local import keeps import-time deps minimal

    session = requests.Session()

    def transport(method: str, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        method = method.upper()
        if method == "GET":
            resp = session.get(url, params=params, timeout=timeout)
        else:
            resp = session.post(url, data=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()

    return transport


@dataclass
class FeatureQueryResult:
    """Parsed result of a feature-layer ``query`` request."""

    features: List[dict] = field(default_factory=list)
    fields: List[dict] = field(default_factory=list)
    geometry_type: Optional[str] = None
    exceeded_transfer_limit: bool = False

    @property
    def attributes(self) -> List[dict]:
        """Just the ``attributes`` dict of each feature."""
        return [f.get("attributes", {}) for f in self.features]

    def __len__(self) -> int:
        return len(self.features)


class ArcGISRestClient:
    """Talk to an ArcGIS portal / server over REST.

    :param portal: portal base URL (default ArcGIS Online).
    :param token: a pre-obtained token, if you have one.
    :param transport: optional injected transport for testing.
    """

    def __init__(
        self,
        portal: str = DEFAULT_PORTAL,
        *,
        token: Optional[str] = None,
        transport: Optional[Transport] = None,
        timeout: float = 30.0,
    ):
        self.portal = portal.rstrip("/")
        self.token = token
        self._transport = transport or _requests_transport(timeout)

    # -- low level ---------------------------------------------------------

    def request(
        self, method: str, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a request, always asking for JSON, and raise on REST errors."""
        params = dict(params or {})
        params.setdefault("f", "json")
        if self.token and "token" not in params:
            params["token"] = self.token

        payload = self._transport(method, url, params)
        _raise_for_rest_error(payload)
        return payload

    # -- auth --------------------------------------------------------------

    def generate_token(
        self,
        username: str,
        password: str,
        *,
        referer: str = "https://www.arcgis.com",
        expiration: int = 60,
    ) -> str:
        """Obtain and store a token via username/password.

        Returns the token and also sets ``self.token`` for subsequent calls.
        """
        url = f"{self.portal}/sharing/rest/generateToken"
        payload = self.request(
            "POST",
            url,
            {
                "username": username,
                "password": password,
                "referer": referer,
                "expiration": expiration,
            },
        )
        token = payload.get("token")
        if not token:
            raise ArcGISRestError("generateToken did not return a token", details=[payload])
        self.token = token
        return token

    # -- feature services --------------------------------------------------

    def query_layer(
        self,
        layer_url: str,
        *,
        where: str = "1=1",
        out_fields: str = "*",
        return_geometry: bool = True,
        result_record_count: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> FeatureQueryResult:
        """Query a feature layer's ``/query`` endpoint.

        :param layer_url: full URL to the layer (``.../FeatureServer/0``).
        """
        params: Dict[str, Any] = {
            "where": where,
            "outFields": out_fields,
            "returnGeometry": str(return_geometry).lower(),
        }
        if result_record_count is not None:
            params["resultRecordCount"] = result_record_count
        if extra:
            params.update(extra)

        payload = self.request("GET", f"{layer_url.rstrip('/')}/query", params)
        return FeatureQueryResult(
            features=payload.get("features", []),
            fields=payload.get("fields", []),
            geometry_type=payload.get("geometryType"),
            exceeded_transfer_limit=bool(payload.get("exceededTransferLimit", False)),
        )

    def get_layer_info(self, layer_url: str) -> Dict[str, Any]:
        """Fetch a layer/service's metadata document."""
        return self.request("GET", layer_url.rstrip("/"))


def _raise_for_rest_error(payload: Dict[str, Any]) -> None:
    error = payload.get("error") if isinstance(payload, dict) else None
    if error:
        raise ArcGISRestError(
            error.get("message", "ArcGIS REST API error"),
            code=error.get("code"),
            details=error.get("details", []),
        )
