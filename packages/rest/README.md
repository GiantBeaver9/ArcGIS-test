# arcgis-rest-client

A thin, dependency-light Python client for the **ArcGIS REST API**. It speaks
the REST endpoints directly (token auth, feature-layer queries, metadata) so
it stays small and easy to embed in tools and automation — no heavy `arcgis`
SDK required.

## Install

```bash
pip install -e ".[dev]"     # from packages/rest
```

Runtime dependency: just `requests`.

## Usage

```python
from arcgis_rest import ArcGISRestClient

client = ArcGISRestClient("https://www.arcgis.com")

# Token auth (optional — public layers need no token)
client.generate_token("USERNAME", "PASSWORD")

# Query a feature layer
result = client.query_layer(
    "https://services.arcgis.com/XXXX/arcgis/rest/services/MyLayer/FeatureServer/0",
    where="STATE = 'CA'",
    out_fields="NAME,POP",
    result_record_count=100,
)

print(len(result), "features")
for attrs in result.attributes:
    print(attrs["NAME"], attrs["POP"])
```

## Why this exists

The full [ArcGIS API for Python](../python) wraps the REST API with a rich
object model but pulls in a large geospatial stack. When you just need to hit a
few REST endpoints from a script, Lambda, or CI job, this client keeps the
footprint tiny.

## Design

- **Injectable transport** — pass your own `transport(method, url, params)`
  callable to test or to plug in a custom HTTP layer. The default uses
  `requests`.
- **Honest errors** — the ArcGIS REST API returns HTTP 200 with an embedded
  `error` object; this client raises `ArcGISRestError` for those.

## Tests

```bash
pytest      # runs fully offline via a fake transport
```
