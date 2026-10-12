#!/usr/bin/env python3
"""Turn a CSV (or plain list) of Pinterest pins into data/boards/<board>.md.

Pinterest doesn't offer a first-party CSV export, but you can hand-build one, or
generate one from a tool like gallery-dl. Expected CSV (with a header row):
    url,note,board
"note" and "board" are optional — pins without a board go to a file called "unsorted".

Usage:
  python parse_pinterest_export.py pins.csv
  python parse_pinterest_export.py links.txt --board "street style"

Stdlib only — no pip install needed. Requires Python 3.10+.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

BOARDS_DIR = Path(__file__).resolve().parent.parent / "data" / "boards"


def slugify(name: str) -> str:
    keep = "".join(ch if ch.isalnum() else "-" for ch in name.strip().lower())
    return "-".join(x for x in keep.split("-") if x) or "unsorted"


def read_csv(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            url = (row.get("url") or row.get("link") or "").strip()
            if not url:
                continue
            rows.append({
                "url": url,
                "note": (row.get("note") or row.get("title")
                         or row.get("description") or "").strip(),
                "board": (row.get("board") or "").strip(),
            })
    return rows


def read_plain(path: Path, default_board: str) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rows.append({"url": line, "note": "", "board": default_board})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="CSV or plain-text list of pin URLs")
    ap.add_argument("--board", default="unsorted",
                    help="board name for a plain list of URLs")
    args = ap.parse_args()

    path = Path(args.file)
    rows = read_csv(path) if path.suffix.lower() == ".csv" else read_plain(path, args.board)

    by_board: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_board[r["board"] or args.board].append(r)

    BOARDS_DIR.mkdir(parents=True, exist_ok=True)
    for board, items in by_board.items():
        md_path = BOARDS_DIR / f"{slugify(board)}.md"
        lines = [f"# {board}", "", f"{len(items)} pins", ""]
        for r in items:
            note = f" — {r['note']}" if r["note"] else ""
            lines.append(f"- [{note or 'pin'}]({r['url']})")
        md_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Wrote {len(items)} pins -> {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
