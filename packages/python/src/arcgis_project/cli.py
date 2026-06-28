"""Command line interface for the project: ``arcgis-project``.

Subcommands:

* ``config``  — print resolved (redacted) settings
* ``whoami``  — connect and show the signed-in user
* ``search``  — search portal content
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from .config import Settings


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arcgis-project",
        description="Helpers for working with ArcGIS content.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("config", help="Print resolved (redacted) configuration.")
    sub.add_parser("whoami", help="Connect and show the signed-in user.")

    search = sub.add_parser("search", help="Search portal content.")
    search.add_argument("--query", default="", help="ArcGIS search query.")
    search.add_argument("--type", dest="item_type", default=None,
                        help="Item type filter, e.g. 'Feature Service'.")
    search.add_argument("--max", dest="max_items", type=int, default=10,
                        help="Max items to return (default: 10).")

    return parser


def _cmd_config(_args) -> int:
    settings = Settings.from_env()
    print(json.dumps(settings.redacted(), indent=2))
    return 0


def _cmd_whoami(_args) -> int:
    from .connection import connect

    gis = connect(Settings.from_env())
    user = getattr(gis.properties, "user", None) or getattr(gis, "users", None)
    me = gis.users.me if hasattr(gis, "users") else None
    if me is not None:
        print(json.dumps(
            {
                "username": getattr(me, "username", None),
                "fullName": getattr(me, "fullName", None),
                "role": getattr(me, "role", None),
                "email": getattr(me, "email", None),
            },
            indent=2,
        ))
    else:
        print("Connected anonymously (no signed-in user).")
    return 0


def _cmd_search(args) -> int:
    from .connection import connect
    from .content import search_items, summarize_items

    gis = connect(Settings.from_env())
    items = search_items(
        gis,
        query=args.query,
        item_type=args.item_type,
        max_items=args.max_items,
    )
    print(json.dumps(summarize_items(items), indent=2))
    return 0


_COMMANDS = {
    "config": _cmd_config,
    "whoami": _cmd_whoami,
    "search": _cmd_search,
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    handler = _COMMANDS[args.command]
    try:
        return handler(args)
    except ImportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
