from arcgis_project.config import DEFAULT_URL, Settings, _mask


def test_defaults_to_anonymous(monkeypatch):
    for var in (
        "ARCGIS_URL",
        "ARCGIS_USERNAME",
        "ARCGIS_PASSWORD",
        "ARCGIS_API_KEY",
        "ARCGIS_PROFILE",
    ):
        monkeypatch.delenv(var, raising=False)

    settings = Settings.from_env(load_env_file=False)
    assert settings.url == DEFAULT_URL
    assert settings.auth_method == "anonymous"


def test_userpass_detected(monkeypatch):
    monkeypatch.setenv("ARCGIS_USERNAME", "alice")
    monkeypatch.setenv("ARCGIS_PASSWORD", "s3cret")
    monkeypatch.delenv("ARCGIS_API_KEY", raising=False)
    monkeypatch.delenv("ARCGIS_PROFILE", raising=False)

    settings = Settings.from_env(load_env_file=False)
    assert settings.auth_method == "userpass"
    assert settings.username == "alice"


def test_api_key_takes_precedence(monkeypatch):
    monkeypatch.setenv("ARCGIS_USERNAME", "alice")
    monkeypatch.setenv("ARCGIS_PASSWORD", "s3cret")
    monkeypatch.setenv("ARCGIS_API_KEY", "abc123key")

    settings = Settings.from_env(load_env_file=False)
    assert settings.auth_method == "api_key"


def test_blank_values_are_ignored(monkeypatch):
    monkeypatch.setenv("ARCGIS_USERNAME", "   ")
    monkeypatch.setenv("ARCGIS_PASSWORD", "")
    monkeypatch.delenv("ARCGIS_API_KEY", raising=False)
    monkeypatch.delenv("ARCGIS_PROFILE", raising=False)

    settings = Settings.from_env(load_env_file=False)
    assert settings.username is None
    assert settings.auth_method == "anonymous"


def test_redacted_hides_secrets():
    settings = Settings(
        url="https://example.com",
        username="alice",
        password="supersecret",
        api_key="keykeykey",
    )
    red = settings.redacted()
    assert red["password"] != "supersecret"
    assert "*" in red["password"]
    assert red["url"] == "https://example.com"


def test_mask_short_and_long():
    assert _mask(None) is None
    assert _mask("ab") == "**"
    masked = _mask("abcdefgh")
    assert masked.startswith("ab") and masked.endswith("gh") and "*" in masked
