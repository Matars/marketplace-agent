# frontend viewer

Static frontend that always renders marketplace-agent results from `latest.json`.

## What it does

- reads `workspaces/default/output/latest.json`
- normalizes variable item shapes into a stable frontend JSON
- renders a polished static UI (`frontend/index.html`) with search/filter/sort
- works on GitHub Pages (no server)

## refresh data for frontend

From repo root:

```bash
python3 frontend/scripts/normalize_latest_json.py \
  --input workspaces/default/output/latest.json \
  --output frontend/data/items-normalized.json
```

Then open `frontend/index.html` locally (or serve statically).

## publish on github pages

Option A: publish root and set Pages source to `/frontend` folder.

Option B: copy `frontend/` to your Pages branch output.

Required committed files:

- `frontend/index.html`
- `frontend/styles.css`
- `frontend/app.js`
- `frontend/data/items-normalized.json`

## notes

- if `latest.json` schema evolves, update only the normalizer script.
- UI reads only normalized JSON, so the frontend stays stable.
