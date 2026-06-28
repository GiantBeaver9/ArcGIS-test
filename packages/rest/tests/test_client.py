import pytest

from arcgis_rest import ArcGISRestClient, ArcGISRestError, FeatureQueryResult


class FakeTransport:
    """Records calls and returns canned responses."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def __call__(self, method, url, params):
        self.calls.append({"method": method, "url": url, "params": params})
        return self._responses.pop(0)


def test_request_injects_f_json_and_token():
    transport = FakeTransport([{"ok": True}])
    client = ArcGISRestClient("https://example.com", token="tok", transport=transport)

    client.request("GET", "https://example.com/foo")

    call = transport.calls[0]
    assert call["params"]["f"] == "json"
    assert call["params"]["token"] == "tok"


def test_rest_error_payload_raises():
    transport = FakeTransport([{"error": {"code": 400, "message": "bad", "details": ["x"]}}])
    client = ArcGISRestClient(transport=transport)

    with pytest.raises(ArcGISRestError) as exc:
        client.request("GET", "https://example.com/foo")
    assert exc.value.code == 400
    assert "bad" in str(exc.value)


def test_generate_token_stores_token():
    transport = FakeTransport([{"token": "abc123", "expires": 999}])
    client = ArcGISRestClient("https://portal", transport=transport)

    token = client.generate_token("alice", "pw")

    assert token == "abc123"
    assert client.token == "abc123"
    # the auth request must hit the generateToken endpoint
    assert transport.calls[0]["url"].endswith("/sharing/rest/generateToken")
    assert transport.calls[0]["method"] == "POST"


def test_generate_token_without_token_raises():
    transport = FakeTransport([{"expires": 999}])
    client = ArcGISRestClient(transport=transport)
    with pytest.raises(ArcGISRestError):
        client.generate_token("alice", "pw")


def test_query_layer_parses_features():
    transport = FakeTransport([
        {
            "geometryType": "esriGeometryPoint",
            "fields": [{"name": "OBJECTID"}],
            "features": [
                {"attributes": {"OBJECTID": 1, "name": "A"}},
                {"attributes": {"OBJECTID": 2, "name": "B"}},
            ],
            "exceededTransferLimit": True,
        }
    ])
    client = ArcGISRestClient(transport=transport)

    result = client.query_layer(
        "https://example.com/FeatureServer/0",
        where="name='A'",
        result_record_count=5,
    )

    assert isinstance(result, FeatureQueryResult)
    assert len(result) == 2
    assert result.geometry_type == "esriGeometryPoint"
    assert result.exceeded_transfer_limit is True
    assert result.attributes == [
        {"OBJECTID": 1, "name": "A"},
        {"OBJECTID": 2, "name": "B"},
    ]
    # query params were passed through
    params = transport.calls[0]["params"]
    assert params["where"] == "name='A'"
    assert params["resultRecordCount"] == 5
    assert transport.calls[0]["url"].endswith("/FeatureServer/0/query")


def test_portal_trailing_slash_normalized():
    client = ArcGISRestClient("https://example.com/", transport=FakeTransport([]))
    assert client.portal == "https://example.com"
