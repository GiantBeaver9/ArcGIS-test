"""Standalone example: connect to a portal and list some content.

Run after configuring .env and installing the arcgis extra:

    pip install -e ".[arcgis]"
    python scripts/example_search.py
"""

from arcgis_project.config import Settings
from arcgis_project.connection import connect
from arcgis_project.content import search_items, summarize_items


def main() -> None:
    settings = Settings.from_env()
    print(f"Connecting to {settings.url} via {settings.auth_method} ...")

    gis = connect(settings)
    items = search_items(gis, query="", item_type="Feature Service", max_items=5)

    for summary in summarize_items(items):
        print(f"- {summary['title']} ({summary['id']})")


if __name__ == "__main__":
    main()
