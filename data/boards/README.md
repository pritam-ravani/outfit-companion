# Pinterest boards

Three ways to get your boards in here. Use whichever works; combine freely.

## 1. Save images manually (always works)
Save pin images to `../inspiration/` (or a subfolder). The companion reads them directly
and extracts the common style threads.

## 2. Paste a board URL
Tell the companion "add this board: <url>". It will try to read it directly (Pinterest
often blocks this) or via the board's RSS feed. If it can't, use method 1 or 3.

## 3. Official API (most reliable for a whole board)
1. Create a free app at https://developers.pinterest.com/
2. Get an OAuth access token with scopes: `boards:read`, `pins:read`
3. Find your board IDs: `python scripts/pinterest_api.py --token TOKEN --list-boards`
4. Pull a board: `python scripts/pinterest_api.py --token TOKEN --board-id ID --name "my board"`

Each board lands here as `<name>.json` (full data) and `<name>.md` (readable summary).
