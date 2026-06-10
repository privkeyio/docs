# PrivKey Docs

Source for **[docs.privkey.io](https://docs.privkey.io)** — a multi-project documentation
portal. Each project keeps its own docs (an mdBook) in its own repo; this repo aggregates
them, applies the shared PrivKey theme, and deploys the result to GitHub Pages.

```
docs.privkey.io/          landing page
docs.privkey.io/keep/     ← built from privkeyio/keep  (docs/ + book.toml)
docs.privkey.io/<name>/   ← one per entry in projects.json
```

## How it works

`build.py` reads `projects.json`, and for each project:

1. clones the public repo at the configured `ref`,
2. injects the shared theme (`theme/privkey.css` + `theme/privkey.js` + the logo),
3. builds its mdBook mounted at `/<name>/`,
4. assembles everything under `public/` with a generated landing page.

No tokens are needed — every project is a public clone. Deployment uses the first-party
GitHub Pages actions (`.github/workflows/deploy.yml`).

## Adding a project

Add an entry to `projects.json`:

```json
{
  "name": "relay",
  "repo": "https://github.com/privkeyio/relay",
  "ref": "main",
  "path": ".",
  "title": "Relay",
  "description": "One-line summary."
}
```

The project repo just needs a `book.toml` and a `docs/` directory with a `SUMMARY.md`
(see `privkeyio/keep` for the pattern). `path` is the directory containing `book.toml`
(default `.`). The theme is injected here, so project repos stay theme-free.

## Local preview

```bash
pip install nothing   # no deps; needs python3 + mdbook on PATH
python3 build.py
python3 -m http.server -d public 8000   # http://localhost:8000
```

## Theme

`theme/privkey.css` and `theme/privkey.js` are the single source of brand styling for every
project's docs. Editing them here restyles the whole portal on the next build.

## One-time hosting setup

1. Repo **Settings → Pages → Source: GitHub Actions**.
2. DNS: `CNAME docs.privkey.io → privkeyio.github.io` (the `CNAME` file is emitted by the build).
