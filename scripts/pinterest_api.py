#!/usr/bin/env python3
"""Pull pins from a Pinterest board using the official Pinterest API v5.

Most reliable way to read a full board, but needs a one-time setup:
  1. Create a free app at https://developers.pinterest.com/
  2. Get an OAuth access token with scopes: boards:read, pins:read
     (Pinterest's "Get started" flow lets you generate a token quickly.)
  3. Find the board ID from its URL: pinterest.com/<user>/<slug>-<board-id>/

Usage:
  python pinterest_api.py --token TOKEN --list-boards              # find your board IDs
  python pinterest_api.py --token TOKEN --board-id 1234567890 --name "my board"

Output: writes data/boards/<name>.json (full data) and data/boards/<name>.md (summary).

Stdlib only — no pip install needed. Requires Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Sandbox is fine for personal use; switch to https://api.pinterest.com/v5 if your app
# is approved for production. Endpoint shapes are identical.
API = "https://api-sandbox.pinterest.com/v5"

BOARDS_DIR = Path(__file__).resolve().parent.parent / "data" / "boards"


def api_get(path: str, token: str, params: dict | None = None) -> dict:
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def paged(fetch, token: str, board_id: str | None = None):
    """Yield items across every page of a Pinterest list endpoint."""
    bookmark = None
    while True:
        params = {"page_size": 25}
        if bookmark:
            params["bookmark"] = bookmark
        data = fetch(token, board_id, params) if board_id else fetch(token, params)
        for item in data.get("items", []):
            yield item
        bookmark = data.get("bookmark")
        if not bookmark:
            break


def fetch_boards(token: str, params: dict) -> dict:
    return api_get("/boards", token, params)


def fetch_pins(token: str, board_id: str, params: dict) -> dict:
    return api_get(f"/boards/{board_id}/pins", token, params)


def pin_url(pin: dict) -> str:
    images = (pin.get("media") or {}).get("images") or {}
    for key in ("600x", "orig", "400x"):
        img = images.get(key)
        if img and img.get("url"):
            return img["url"]
    return ""


def pin_to_md(pin: dict) -> str:
    title = (pin.get("title") or "").strip() or "(untitled)"
    note = (pin.get("description") or "").strip()
    link = pin.get("link") or pin.get("url") or ""
    img = pin_url(pin)
    lines = [f"### {title}", ""]
    if note:
        lines += [note, ""]
    lines.append(f"- link: {link}")
    if img:
        lines.append(f"- image: {img}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--token", required=True, help="Pinterest OAuth access token")
    ap.add_argument("--list-boards", action="store_true",
                    help="list your boards and their IDs, then exit")
    ap.add_argument("--board-id", help="board ID to pull (find it via --list-boards)")
    ap.add_argument("--name", help="name to save the board under (used in filenames)")
    args = ap.parse_args()

    if args.list_boards:
        for board in paged(fetch_boards, args.token):
            print(f"{board.get('id', '?')}  {board.get('name', '(unnamed)')}")
        return 0

    if not args.board_id:
        print("Pass --board-id (find it with --list-boards), or use --list-boards.",
              file=sys.stderr)
        return 2

    name = args.name or f"board-{args.board_id}"
    pins = list(paged(fetch_pins, args.token, args.board_id))

    BOARDS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = BOARDS_DIR / f"{name}.json"
    md_path = BOARDS_DIR / f"{name}.md"

    json_path.write_text(json.dumps(pins, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [f"# {name}", "", f"{len(pins)} pins", ""]
    md += [pin_to_md(p) + "\n" for p in pins]
    md_path.write_text("\n".join(md), encoding="utf-8")

    print(f"Saved {len(pins)} pins:")
    print(f"  {json_path}")
    print(f"  {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
