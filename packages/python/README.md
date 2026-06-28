# ArcGIS Project

A starter project built on the [ArcGIS API for Python](https://developers.arcgis.com/python/)
for connecting to ArcGIS Online / ArcGIS Enterprise, querying content, and
running geospatial analysis and automation.

It is structured as a small, importable package (`arcgis_project`) plus a thin
CLI, so you can grow it into notebooks, scheduled jobs, or a reusable toolkit
shared across repos.

## Features

- Centralized, environment-driven configuration (`arcgis_project.config`)
- A single helper to authenticate a GIS connection (`arcgis_project.connection`)
- Content helpers for searching and summarizing items (`arcgis_project.content`)
- A `arcgis-project` CLI entry point for quick checks from the terminal
- Tests that run **without** network access or the heavy `arcgis` dependency

## Requirements

- Python 3.9+
- An ArcGIS Online or ArcGIS Enterprise account (for anything that hits the network)

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install (dev install with test deps)
pip install -e ".[dev]"

# 3. Configure credentials
cp .env.example .env
# then edit .env with your portal URL / username / password (or API key)
```

> The `arcgis` package is large and pulls in geospatial native libraries.
> It is an **optional** dependency here so you can develop and test core logic
> without it. Install it when you need live portal access:
>
> ```bash
> pip install -e ".[arcgis]"
> ```

## Usage

### CLI

```bash
# Show resolved (non-secret) configuration
arcgis-project config

# Connect and print info about the signed-in user
arcgis-project whoami

# Search your org's content
arcgis-project search --query "owner:me" --max 10
```

### As a library

```python
from arcgis_project.config import Settings
from arcgis_project.connection import connect
from arcgis_project.content import search_items

gis = connect(Settings.from_env())
items = search_items(gis, query="type:Feature Service", max_items=25)
for item in items:
    print(item.title, item.id)
```

## Project layout

```
.
├── src/arcgis_project/      # the importable package
│   ├── config.py            # Settings loaded from env / .env
│   ├── connection.py        # connect() -> GIS
│   ├── content.py           # search / summarize helpers
│   └── cli.py               # `arcgis-project` command
├── scripts/                 # standalone example scripts
├── notebooks/               # Jupyter notebooks (kept empty in git)
├── tests/                   # pytest suite (no network needed)
└── pyproject.toml
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).
