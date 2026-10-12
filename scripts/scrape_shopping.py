#!/usr/bin/env python3
"""Extract product details from a shopping URL (name, price, brand, image, availability).

Tries, in order:
  1. JSON-LD structured data (<script type="application/ld+json"> of type Product)
  2. Open Graph / product meta tags (og:title, og:image, product:price:amount, ...)

Stdlib only — no pip install needed. Many sites block scripts entirely; if this returns
nothing, use Claude's built-in WebFetch on the page instead.

Usage:
  python scrape_shopping.py https://example.com/item/123
  python scrape_shopping.py https://example.com/item/123 --json
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (compatible; fashion-companion/1.0)"}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_jsonld(page: str) -> list[dict]:
    """Return parsed JSON-LD blocks, flattening @graph arrays."""
    out = []
    pattern = re.compile(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S)
    for m in pattern.finditer(page):
        raw = html.unescape(m.group(1)).strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            out.extend(data)
        elif isinstance(data, dict):
            if isinstance(data.get("@graph"), list):
                out.extend(data["@graph"])
            else:
                out.append(data)
    return out


def meta(page: str, key: str) -> str:
    pat = re.escape(key)
    m = (re.search(rf'<meta[^>]+(?:property|name)=["\']{pat}["\'][^>]+content=["\'](.*?)["\']', page, re.S)
         or re.search(rf'<meta[^>]+content=["\'](.*?)["\'][^>]+(?:property|name)=["\']{pat}["\']', page, re.S))
    return html.unescape(m.group(1)).strip() if m else ""


def money(price: str, currency: str) -> str:
    price = price.strip()
    return f"{currency} {price}" if currency and price else price


def product_from_jsonld(blocks: list[dict]) -> dict:
    for b in blocks:
        if b.get("@type") not in ("Product", "ProductGroup", "IndividualProduct", "Clothing"):
            continue
        offers = b.get("offers") or {}
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        brand = b.get("brand") or {}
        if isinstance(brand, dict):
            brand = brand.get("name", "")
        image = b.get("image")
        if isinstance(image, list):
            image = image[0] if image else ""
        return {
            "name": b.get("name", ""),
            "brand": str(brand),
            "price": money(str(offers.get("price", "")),
                           str(offers.get("priceCurrency", ""))),
            "currency": offers.get("priceCurrency", ""),
            "availability": str(offers.get("availability", "")).rsplit("/", 1)[-1],
            "image": image,
        }
    return {}


def product_from_meta(page: str) -> dict:
    price = meta(page, "product:price:amount") or meta(page, "og:price:amount")
    currency = meta(page, "product:price:currency") or meta(page, "og:price:currency")
    return {
        "name": meta(page, "og:title"),
        "brand": meta(page, "product:brand"),
        "price": money(price, currency),
        "currency": currency,
        "availability": meta(page, "product:availability"),
        "image": meta(page, "og:image"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true", help="print as JSON instead of text")
    args = ap.parse_args()

    try:
        page = fetch(args.url)
    except Exception as e:  # noqa: BLE001
        print(f"Could not fetch {args.url}: {e}", file=sys.stderr)
        return 1

    info = product_from_jsonld(extract_jsonld(page)) or product_from_meta(page)

    if not (info.get("name") or info.get("price") or info.get("image")):
        print("No product data found — the site may block scripts or lack structured data.",
              file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        for key in ("name", "brand", "price", "availability", "image"):
            if info.get(key):
                print(f"{key}: {info[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
