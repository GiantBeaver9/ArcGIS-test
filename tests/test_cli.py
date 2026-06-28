import json

from arcgis_project.cli import main


def test_config_command_outputs_redacted_json(monkeypatch, capsys):
    monkeypatch.setenv("ARCGIS_USERNAME", "alice")
    monkeypatch.setenv("ARCGIS_PASSWORD", "supersecret")
    monkeypatch.delenv("ARCGIS_API_KEY", raising=False)

    rc = main(["config"])
    out = capsys.readouterr().out
    data = json.loads(out)

    assert rc == 0
    assert data["auth_method"] == "userpass"
    assert data["password"] != "supersecret"


def test_search_without_arcgis_installed_errors_cleanly(monkeypatch, capsys):
    # If 'arcgis' isn't importable, the CLI should exit 2 with a helpful message
    # rather than a traceback. We can't assume the package is absent in every
    # environment, so only assert behavior when it's genuinely missing.
    import importlib.util

    if importlib.util.find_spec("arcgis") is not None:
        return  # arcgis present; skip the "missing dependency" path

    rc = main(["search", "--query", "owner:me"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "arcgis" in err
