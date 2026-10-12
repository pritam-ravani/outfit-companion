# Fashion Companion

A Claude Code **skill** that acts as your personal stylist. It builds a living profile
of you — body shape, color season, taste, budget, and climate — then turns that into
concrete, personalized advice: what to wear, what to buy, and what's actually worth
your attention in fashion.

## What it does

- **Outfit advice** — "what should I wear" for any occasion, built from your own
  wardrobe first, then a genuine gap only if needed.
- **Wardrobe & capsule curation** — track what you own, spot the gaps, and assemble
  capsules that flow across your three modes (office / occasion / street).
- **Shopping help** — collect and compare products, respect your budget and no-go list,
  and name a specific pick instead of dumping links.
- **Trend reports** — what's in right now, filtered to what actually flatters *you*.
- **Inspiration ingestion** — pull Pinterest/Cosmos boards (saved images, board URL, or
  the official API) and distil them into reusable silhouettes, colors, and formulas.
- **Image generation** — render outfits *on you* from your reference photos via a local
  image model, then vision-review the results for fit and palette.
- **Find the fit / shop the look** — turn a generated outfit (or any outfit image) into
  a shoppable list of real pieces, and match it against the looks you already have.

## How it works

Every recommendation traces back to `data/profile.md` — the single source of truth for
your body, coloring, taste, budget and climate. The skill reads it before advising and
writes to it when you tell it something new. The *how to style* knowledge lives
separately in `references/`, so it stays general while the advice stays personal.

## Project layout

| Path | What's in it |
|------|--------------|
| `SKILL.md` | The skill definition and its workflows |
| `data/profile.md` | Body, coloring, taste, budget, climate — source of truth |
| `data/wardrobe.md` | Items you already own |
| `data/wishlist.md` | Product links you're considering |
| `data/collections/` | Profile-filtered piece & formula lists per mode |
| `data/inspiration/` | Saved fashion images (pins, lookbooks, street style) |
| `data/generated/` | Generated "on me" outfit renders, catalog, and local gallery |
| `data/moodboards/` | Self-contained HTML moodboards per style theme |
| `references/` | Styling knowledge — color, body types, fit, trends, weather |
| `scripts/` | Optional Python helpers (Pinterest API, shopping scrape) |

## Install

Skills are discovered from a `skills/` directory. From inside this folder:

**Global (available everywhere):**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force . "$env:USERPROFILE\.claude\skills\fashion-companion"
```

**Project-local (only this project):**
```powershell
New-Item -ItemType Directory -Force ".claude\skills" | Out-Null
Copy-Item -Recurse -Force . ".claude\skills\fashion-companion"
```

Restart Claude Code, then just talk: *"what should I wear to a wedding"*, *"plan my
capsule wardrobe"*, *"add this Pinterest board"*, *"find the fit from this outfit"*.

## First-time setup

1. Copy `data/profile.example.md` → `data/profile.md` and fill it in — or just tell
   Claude about yourself and it will fill it in.
2. Copy `data/wardrobe.example.md` → `data/wardrobe.md` and add what you own.
3. Save some inspiration: drop images into `data/inspiration/`, or point Claude at a board.

> Your real data files (`profile.md`, `wardrobe.md`, photos, generated renders, and the
> rest) are git-ignored by default, so they stay local and never get published.

## Optional: enable the Python helpers

The skill works fully without Python (it uses Claude's built-in web/file tools). Install
Python to unlock the bundled scripts:

| Script | What it does | Needs |
|--------|--------------|-------|
| `scripts/pinterest_api.py` | Pull a full Pinterest board via the official API | Python 3 + a Pinterest OAuth token |
| `scripts/parse_pinterest_export.py` | Convert a CSV/list of pins into `data/boards/*.md` | Python 3 |
| `scripts/scrape_shopping.py` | Extract product name/price/image from a URL | Python 3 (stdlib only) |

No third-party packages required — the scripts use Python's standard library.

## Privacy

`data/photos/`, `data/profile.md`, and `data/generated/` hold personal data and your
likeness. Keep them private — don't commit them to a public repo, and don't let the
skill publish or share them anywhere.
