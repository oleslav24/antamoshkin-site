# GEO / LLM implementation

## Baseline and architecture

The site is a dependency-free static site generator: Markdown source pages under `content/<lang>/`, a bibliography source parsed by `scripts/build_site.py`, and committed HTML in `public/` for Cloudflare Pages. It is SSG, not an SPA; public content is delivered in the initial HTML response. Existing `/en/*.html` and `/ru/*.html` routes remain unchanged.

Metadata, canonical URLs, hreflang, Open Graph tags, JSON-LD, `sitemap.xml`, and `robots.txt` are generated in `scripts/build_site.py`. Publications are parsed from the local GOST bibliography source, with English localization data in `content/en/publications.json`.

## Problems found

- `robots.txt` did not name AI crawlers explicitly.
- The Person entity used a generic fragment identifier and did not expose all existing academic identifiers.
- There were no entity pages for the professional profile, key projects, expertise, or individual publications.
- The publications page emitted every citation style as hidden HTML, creating duplicate bibliographic text for crawlers.
- Hosting-level canonical-host enforcement cannot be guaranteed by static HTML alone.

## Implemented decisions

- `https://oleslav.com` remains the canonical host; every generated canonical URL uses it.
- `public/_redirects` requests non-www and HTTP to HTTPS non-www redirects where Cloudflare Pages applies these host rules.
- `robots.txt` explicitly allows OAI-SearchBot, GPTBot, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, and Google-Extended.
- The canonical Person is `https://oleslav.com/#oleslav-antamoshkin`; its schema contains existing ORCID, Scopus, Web of Science, RSCI, and SPIN identifiers and verified profile links.
- New static entity pages are generated for `/en/about`, `/ru/about`, AirScope, Siberiana, six expertise topics, and selected/recent/DOI-bearing publications.
- Publication pages use `ScholarlyArticle` schema and DOI links where a DOI is available.
- Initial publication-list HTML now contains one canonical GOST citation only. The citation-format switcher derives alternative formats in the browser from structured bibliographic fields after a user action.
- `llms.txt`, sitemap routes, breadcrumbs, hreflang pairs, and a build-output validation script are generated or checked as part of the static build.

## Changed files

- `scripts/build_site.py`
- `scripts/verify_geo.py`
- `content/en/about.md`
- `content/ru/about.md`
- `public/styles.css`
- generated files under `public/`

## Local verification

```powershell
python -B scripts\build_site.py
python -B scripts\verify_geo.py
```

## Required after deployment

1. In Cloudflare, confirm a redirect rule or zone configuration sends `www.oleslav.com` and all HTTP variants to `https://oleslav.com`, preserving path and query string. On 29 Sep 2026, `https://www.oleslav.com/` still returned `200` rather than a redirect, while HTTP variants returned `301`. Cloudflare Pages `_redirects` is included, but DNS/zone settings can override it; add a zone-level 301/308 redirect if the deployment does not correct this.
2. Confirm Cloudflare WAF/Bot Management does not challenge the explicitly allowed public crawler user agents on HTML, `robots.txt`, `sitemap.xml`, and `llms.txt`.
3. Submit the canonical sitemap to Google Search Console and Bing Webmaster Tools. IndexNow publication is intentionally not triggered during local builds; after deployment, submit changed production URLs with the included script or from the deployment workflow.
4. Consider `X-Robots-Tag: noindex` for the generated citation-list PDFs only if Cloudflare header rules can target `/downloads/publications-*.pdf` without affecting genuine scholarly documents.

## IndexNow

The stable verification file is generated at `/<key>.txt`. After production deployment, submit only changed canonical URLs, for example:

```powershell
python -B scripts\indexnow.py https://oleslav.com/en/about https://oleslav.com/en/projects/airscope
```

The script rejects preview, localhost, query-string, and non-canonical URLs. It is deliberately not called by `build_site.py`.
