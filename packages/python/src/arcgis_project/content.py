"""Helpers for searching and summarizing portal content.

These functions accept an already-connected ``GIS`` object so they stay
testable with a lightweight stand-in (anything exposing ``.content.search``).
"""

from __future__ import annotations

from typing import Any, List


def search_items(
    gis: Any,
    query: str = "",
    *,
    item_type: str | None = None,
    max_items: int = 50,
) -> List[Any]:
    """Search the portal for items.

    :param gis: a connected ``GIS`` object.
    :param query: an ArcGIS search query string (e.g. ``"owner:me"``).
    :param item_type: optional item type filter (e.g. ``"Feature Service"``).
    :param max_items: maximum number of items to return.
    """
    return gis.content.search(
        query=query,
        item_type=item_type,
        max_items=max_items,
    )


def summarize_item(item: Any) -> dict:
    """Return a small, JSON-friendly summary of a portal item."""
    return {
        "id": getattr(item, "id", None),
        "title": getattr(item, "title", None),
        "type": getattr(item, "type", None),
        "owner": getattr(item, "owner", None),
        "num_views": getattr(item, "numViews", None),
    }


def summarize_items(items: List[Any]) -> List[dict]:
    """Summarize a list of items."""
    return [summarize_item(item) for item in items]
