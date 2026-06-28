from arcgis_project.config import Settings
from arcgis_project.connection import gis_kwargs


def test_gis_kwargs_anonymous():
    settings = Settings(url="https://example.com")
    assert gis_kwargs(settings) == {"url": "https://example.com"}


def test_gis_kwargs_userpass():
    settings = Settings(url="https://example.com", username="alice", password="pw")
    assert gis_kwargs(settings) == {
        "url": "https://example.com",
        "username": "alice",
        "password": "pw",
    }


def test_gis_kwargs_api_key():
    settings = Settings(url="https://example.com", api_key="k")
    assert gis_kwargs(settings) == {"url": "https://example.com", "api_key": "k"}


def test_gis_kwargs_profile():
    settings = Settings(url="https://example.com", profile="work")
    assert gis_kwargs(settings) == {"url": "https://example.com", "profile": "work"}
