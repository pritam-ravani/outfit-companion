# Style Collections — curated from your data

Three collections (office, occasion, street), each a profile-filtered list of the
specific pieces and outfit formulas worth downloading and saving. Built from web
search, then filtered through **your** profile before anything made the list.

## The filter every item passes

- **Color — Deep Autumn:** olive, khaki, brown, maroon/rust, cream, charcoal, deep
  teal, dusty pink. Rejected: stark white, icy pastels, cool grey, jet black as the
  lead (soft black/charcoal is fine).
- **Fit — straight/relaxed, never skinny:** room in the thigh, boxy-through-loose
  tops, no cigarette/skinny trousers.
- **Climate — home hot + humid:** breathable cotton/linen/chambray first; knit and
  outerwear only as AC/evening/cold-trip layers.
- **Signature:** (fill in from your profile) — your standout accessory or repeatable
  accent, the one silhouette that always flatters, and your dressy anchor.

## How it maps to your files

| Path | What it is |
|------|-----------|
| `collections/office.md` | Smart-casual work pieces + formulas |
| `collections/occasion.md` | Going-out / festive pieces + formulas |
| `collections/street.md` | Streetwear pieces + formulas |
| `../inspiration/<mode>/` | Downloaded images land here (per mode) |
| `../moodboards/<mode>.html` | Visual moodboard for that mode |

## Status

- ✅ Search done, choices made, lists written (the three files here).
- ⏳ **Image download pending** — needs the browser connected to your logged-in Edge
  (Playwright `--extension`). Each mode file ends with a **Download queue** of the
  exact pins to grab once the browser is live.

When images are downloaded, drop them in `data/inspiration/<mode>/` and they'll slot
into the matching moodboard's Inspiration section.
