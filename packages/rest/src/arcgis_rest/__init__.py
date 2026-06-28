"""A thin, dependency-light client for the ArcGIS REST API.

Unlike the full ``arcgis`` SDK, this package speaks the REST API directly so
it stays small and easy to embed in tools and automation.
"""

from .client import ArcGISRestClient, FeatureQueryResult
from .errors import ArcGISRestError

__version__ = "0.1.0"
__all__ = ["ArcGISRestClient", "FeatureQueryResult", "ArcGISRestError", "__version__"]
