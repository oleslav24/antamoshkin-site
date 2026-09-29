from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CANONICAL_HOST = "https://oleslav.com"
PERSON_ID = "https://oleslav.com/#oleslav-antamoshkin"


class PageAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.titles = 0
        self.descriptions = 0
        self.canonicals: list[str] = []
        self.hreflangs: set[str] = set()
        self.h1_count = 0
        self._in_h1 = False
        self.json_ld: list[str] = []
        self._in_json_ld = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.titles += 1
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.descriptions += 1
        if tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href", ""))
        if tag == "link" and values.get("rel") == "alternate" and values.get("hreflang"):
            self.hreflangs.add(values["hreflang"])
        if tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self._in_h1 = False
        if tag == "script":
            self._in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self.json_ld.append(data)


def check_page(page: Path) -> list[str]:
    audit = PageAudit()
    source = page.read_text(encoding="utf-8")
    audit.feed(source)
    errors: list[str] = []
    label = page.relative_to(PUBLIC).as_posix()
    if audit.titles != 1:
        errors.append(f"{label}: expected one title")
    if audit.descriptions != 1:
        errors.append(f"{label}: missing description")
    if len(audit.canonicals) != 1 or not audit.canonicals[0].startswith(CANONICAL_HOST):
        errors.append(f"{label}: invalid canonical")
    if "noindex" in source.lower():
        errors.append(f"{label}: unexpectedly noindex")
    if audit.h1_count != 1:
        errors.append(f"{label}: expected one h1, got {audit.h1_count}")
    if page.parts[-3:-1] in [("en", "about"), ("ru", "about")] or "expertise" in page.parts or "projects" in page.parts or "publications" in page.parts:
        if not {"en", "ru", "x-default"}.issubset(audit.hreflangs):
            errors.append(f"{label}: missing hreflang pair")
    person_seen = False
    for payload in audit.json_ld:
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON-LD ({exc})")
            continue
        graph = data.get("@graph", [data])
        person_seen = person_seen or any(item.get("@id") == PERSON_ID for item in graph if isinstance(item, dict))
    if not person_seen:
        errors.append(f"{label}: canonical Person entity missing")
    return errors


def main() -> None:
    errors: list[str] = []
    pages = [page for page in PUBLIC.rglob("*.html") if not page.name.startswith("yandex_")]
    for page in pages:
        if page.name == "404.html":
            continue
        errors.extend(check_page(page))

    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
    for agent in ("OAI-SearchBot", "GPTBot", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Google-Extended"):
        if f"User-agent: {agent}\nAllow: /" not in robots:
            errors.append(f"robots.txt: {agent} is not explicitly allowed")
    if "Sitemap: https://oleslav.com/sitemap.xml" not in robots:
        errors.append("robots.txt: sitemap missing")

    sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    for url in ("https://oleslav.com/en/about", "https://oleslav.com/ru/about", "https://oleslav.com/en/projects/airscope"):
        if f"<loc>{url}</loc>" not in sitemap:
            errors.append(f"sitemap.xml: {url} missing")

    publications = (PUBLIC / "en" / "publications.html").read_text(encoding="utf-8")
    if re.search(r'data-citation-style="(?:apa|mla|chicago|harvard|ieee|vancouver|bibtex)"', publications):
        errors.append("publications: inactive citation formats were rendered into the initial DOM")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"GEO_CHECK=OK ({len(pages) - 1} indexable HTML pages)")


if __name__ == "__main__":
    main()
