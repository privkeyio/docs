#!/usr/bin/env python3
"""Build the docs.privkey.io portal.

For each project in projects.json: clone the public repo, inject the shared
PrivKey theme (theme/privkey.css + theme/privkey.js), build its mdBook mounted
at /<name>/, and assemble everything under public/ alongside a landing page.

No tokens required: all projects are public clones. Run: python3 build.py
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
THEME = ROOT / "theme"
LOGO = ROOT / "assets" / "brand-icon.png"
WORK = ROOT / ".work"
DOMAIN = "docs.privkey.io"


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def build_project(p):
    name, repo, ref = p["name"], p["repo"], p.get("ref", "main")
    dest = WORK / name
    if dest.exists():
        shutil.rmtree(dest)
    run(["git", "clone", "--depth", "1", "--branch", ref, repo, str(dest)])

    bookdir = dest / p.get("path", ".")
    book_toml = bookdir / "book.toml"
    if not book_toml.exists():
        print(f"!! {name}: no book.toml (ref {ref}), skipping")
        return False

    # Inject the shared theme into the clone. The sidebar logo is per-project:
    # a project's own icon if it has one, else the PrivKey logo.
    logo_url = f"/{name}/brand-logo.png" if p.get("icon") else "/brand-icon.png"
    tdir = bookdir / "_theme"
    tdir.mkdir(exist_ok=True)
    shutil.copy(THEME / "privkey.css", tdir / "privkey.css")
    js = (THEME / "privkey.js").read_text().replace("__PK_LOGO_URL__", logo_url)
    (tdir / "privkey.js").write_text(js)

    # Patch book.toml: drop any existing site-url/additional-* then set ours,
    # mounting the book at /<name>/ and wiring in the shared theme.
    text = book_toml.read_text()
    text = re.sub(
        r"(?m)^\s*(site-url|additional-css|additional-js|default-theme|preferred-dark-theme)\s*=.*\n",
        "",
        text,
    )
    inject = (
        'default-theme = "navy"\n'
        'preferred-dark-theme = "navy"\n'
        'additional-css = ["_theme/privkey.css"]\n'
        'additional-js = ["_theme/privkey.js"]\n'
        f'site-url = "/{name}/"\n'
    )
    if "[output.html]" in text:
        text = text.replace("[output.html]\n", "[output.html]\n" + inject, 1)
    else:
        text += "\n[output.html]\n" + inject
    book_toml.write_text(text)

    run(["mdbook", "build", str(bookdir)])

    target = PUBLIC / name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(bookdir / "book", target)

    icon = p.get("icon")
    if icon:
        shutil.copy(ROOT / "assets" / "icons" / icon, target / "brand-logo.png")
    return True


def write_landing(projects):
    cards = "\n".join(
        f'    <a class="card" href="/{p["name"]}/">'
        f'<h2>{p.get("title", p["name"])}</h2>'
        f'<p>{p.get("description", "")}</p></a>'
        for p in projects
    )
    (PUBLIC / "index.html").write_text(LANDING.replace("{{CARDS}}", cards))


def main():
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir()

    cfg = json.loads((ROOT / "projects.json").read_text())
    built = [p for p in cfg["projects"] if build_project(p)]

    shutil.copy(LOGO, PUBLIC / "brand-icon.png")
    write_landing(built)
    (PUBLIC / "CNAME").write_text(DOMAIN + "\n")
    (PUBLIC / ".nojekyll").write_text("")

    print("Built:", ", ".join(p["name"] for p in built) or "(none)")


LANDING = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>PrivKey Docs</title>
<link rel="icon" type="image/png" href="/brand-icon.png" />
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet" />
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #e7ebf2;
    background:
      radial-gradient(1100px 560px at 50% -10%, #11241a 0%, transparent 60%),
      linear-gradient(135deg, #1a1a1a 0%, #0d1117 50%, #161b22 100%);
  }
  .wrap { max-width: 56rem; margin: 0 auto; padding: 4.5rem 1.25rem 5rem; }
  .brand { display: flex; align-items: center; gap: .85rem; margin-bottom: 1.4rem; }
  .brand img { height: 72px; width: auto;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,.45)); }
  .brand span { font-family: 'Space Grotesk', sans-serif; font-weight: 700;
    font-size: 2.4rem; letter-spacing: -.02em; color: #fff; }
  .lede { color: #9aa4b2; font-size: 1.1rem; margin: 0 0 2.5rem; max-width: 34rem; }
  .grid { display: grid; gap: 1rem;
    grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr)); }
  .card {
    display: block; text-decoration: none; color: inherit;
    background: #11161d; border: 1px solid #20262f; border-radius: 12px;
    padding: 1.2rem 1.3rem; transition: border-color .15s, transform .15s;
  }
  .card:hover { border-color: #27ae60; transform: translateY(-2px); }
  .card h2 { font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem;
    margin: 0 0 .35rem; color: #fff; }
  .card p { margin: 0; color: #9aa4b2; font-size: .92rem; line-height: 1.45; }
  footer { margin-top: 3rem; color: #6b7686; font-size: .85rem; }
  footer a { color: #3ad07f; text-decoration: none; }
</style>
</head>
<body>
  <main class="wrap">
    <div class="brand">
      <img src="/brand-icon.png" alt="PrivKey" />
      <span>PrivKey</span>
    </div>
    <p class="lede">Documentation for security-first, open-source tools for Bitcoin, Lightning, and Nostr.</p>
    <div class="grid">
{{CARDS}}
    </div>
    <footer>Source on <a href="https://github.com/privkeyio">GitHub</a>.</footer>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    main()
