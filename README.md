# PrivKey Docs

Source for **[docs.privkey.io](https://docs.privkey.io)**. Each project keeps its own mdBook
in its own repo; `build.py` clones them, applies the shared theme, and deploys to GitHub
Pages. Each lands at `docs.privkey.io/<name>/`.

## Add a project

Add an entry to `projects.json`:

```json
{
  "name": "relay",
  "repo": "https://github.com/privkeyio/relay",
  "ref": "main",
  "title": "Relay",
  "description": "One-line summary."
}
```

The repo just needs a `book.toml` and a `docs/` directory with a `SUMMARY.md` (see
`privkeyio/keep`). The theme is injected at build time, so project repos stay theme-free.

## Develop

```bash
python3 build.py                          # needs python3 + mdbook on PATH
python3 -m http.server -d public 8000     # preview at localhost:8000
```

Deploy is automatic via `.github/workflows/deploy.yml` (on push, daily cron, or manual
dispatch). Brand styling lives in `theme/privkey.css` and `theme/privkey.js`.
