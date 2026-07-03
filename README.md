# Personal Site

Static bilingual profile site for Oleslav Antamoshkin.

## Structure

- `content/ru/*.md` - Russian Markdown source pages.
- `content/en/*.md` - English Markdown source pages.
- `scripts/build_site.py` - dependency-free Markdown-to-HTML builder used locally.
- `public/` - generated static site ready for hosting.

## Local Build

Run from this repository root:

```powershell
python -B scripts\build_site.py
```

Open `public/index.html` in a browser.

## Cloudflare Pages

Use these settings:

- Framework preset: `None`
- Build command: leave empty
- Build output directory: `public`

The generated `public/` directory is committed, so Cloudflare Pages can publish it directly from GitHub.

## Publication Boundary

The repository contains only public profile site content and generated static files. Private working notes, questionnaires, temporary extraction files, and source documents stay outside this site repository.
