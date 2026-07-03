from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = ROOT.parent
CONTENT_DIR = ROOT / "content"
PUBLIC_DIR = ROOT / "public"
BIBLIOGRAPHY_SOURCE = WORKSPACE_ROOT / "tmp" / "Bibliography - Oleslav Antamoshkin - GOST.md"

PAGES = [
    ("index", {"ru": "Главная", "en": "Home"}),
    ("projects", {"ru": "Проекты", "en": "Projects"}),
    ("research", {"ru": "Исследования", "en": "Research"}),
    ("publications", {"ru": "Публикации", "en": "Publications"}),
    ("experience", {"ru": "Роли", "en": "Roles"}),
    ("contacts", {"ru": "Контакты", "en": "Contacts"}),
]

CITATION_STYLES = [
    ("gost", {"ru": "ГОСТ", "en": "GOST"}),
    ("apa", {"ru": "APA 7", "en": "APA 7"}),
    ("mla", {"ru": "MLA 9", "en": "MLA 9"}),
    ("chicago", {"ru": "Chicago", "en": "Chicago"}),
    ("harvard", {"ru": "Harvard", "en": "Harvard"}),
    ("ieee", {"ru": "IEEE", "en": "IEEE"}),
    ("vancouver", {"ru": "Vancouver", "en": "Vancouver"}),
    ("bibtex", {"ru": "BibTeX", "en": "BibTeX"}),
]

SECTION_LABELS = {
    "Научные работы": {
        "ru": "Научные работы",
        "en": "Research Publications",
    },
    "Авторские свидетельства и регистрации ПО/БД": {
        "ru": "Авторские свидетельства и регистрации ПО/БД",
        "en": "Software and Database Registrations",
    },
    "Учебно-методические работы": {
        "ru": "Учебно-методические работы",
        "en": "Teaching and Methodological Works",
    },
}

LANG_META = {
    "ru": {
        "html_lang": "ru",
        "name": "RU",
        "other": "en",
        "skip": "К содержанию",
        "site": "Олеслав Антамошкин",
        "role": "Software engineering · AI · distributed systems",
        "footer": "Публичная визитка. Источники: локальные профильные карточки проекта.",
    },
    "en": {
        "html_lang": "en",
        "name": "EN",
        "other": "ru",
        "skip": "Skip to content",
        "site": "Oleslav Antamoshkin",
        "role": "Software engineering · AI · distributed systems",
        "footer": "Public profile site. Sources: local project profile notes.",
    },
}


def page_href(slug: str) -> str:
    return "index.html" if slug == "index" else f"{slug}.html"


def render_inline(text: str) -> str:
    code_spans: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        code_spans.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00CODE{len(code_spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)
    escaped = html.escape(text)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.escape(match.group(2), quote=True)
        attrs = ""
        if href.startswith("http"):
            attrs = ' target="_blank" rel="noreferrer"'
        return f'<a href="{href}"{attrs}>{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)

    for index, code in enumerate(code_spans):
        escaped = escaped.replace(f"\x00CODE{index}\x00", code)
    return escaped


def render_table(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for raw in lines:
        stripped = raw.strip().strip("|")
        rows.append([cell.strip() for cell in stripped.split("|")])

    if not rows:
        return ""

    header = rows[0]
    body_rows = rows[2:] if len(rows) > 1 and set(rows[1][0]) <= {"-", ":"} else rows[1:]

    parts = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    for cell in header:
        parts.append(f"<th>{render_inline(cell)}</th>")
    parts.append("</tr></thead>")

    if body_rows:
        parts.append("<tbody>")
        for row in body_rows:
            parts.append("<tr>")
            for cell in row:
                parts.append(f"<td>{render_inline(cell)}</td>")
            parts.append("</tr>")
        parts.append("</tbody>")

    parts.append("</table></div>")
    return "\n".join(parts)


def markdown_to_html(markdown: str) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    lines = markdown.splitlines()
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            joined = " ".join(line.strip() for line in paragraph)
            output.append(f"<p>{render_inline(joined)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_list()
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            flush_paragraph()
            close_list()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            output.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            output.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped == "---":
            flush_paragraph()
            close_list()
            output.append("<hr>")
            i += 1
            continue

        unordered = re.match(r"^-\s+(.+)$", stripped)
        if unordered:
            flush_paragraph()
            if list_type != "ul":
                close_list()
                output.append("<ul>")
                list_type = "ul"
            output.append(f"<li>{render_inline(unordered.group(1))}</li>")
            i += 1
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered:
            flush_paragraph()
            if list_type != "ol":
                close_list()
                output.append("<ol>")
                list_type = "ol"
            output.append(f"<li>{render_inline(ordered.group(1))}</li>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_list()
            quote = stripped.lstrip(">").strip()
            output.append(f"<blockquote>{render_inline(quote)}</blockquote>")
            i += 1
            continue

        close_list()
        paragraph.append(line)
        i += 1

    flush_paragraph()
    close_list()
    return "\n".join(output)


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def clean_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def ru_plural(number: int, one: str, few: str, many: str) -> str:
    if number % 10 == 1 and number % 100 != 11:
        return one
    if 2 <= number % 10 <= 4 and not 12 <= number % 100 <= 14:
        return few
    return many


def ensure_period(value: str) -> str:
    value = value.strip()
    if value and value[-1] not in ".!?":
        return f"{value}."
    return value


def extract_year(citation: str) -> str:
    years = re.findall(r"\b(?:19|20)\d{2}\b", citation)
    return years[0] if years else "n.d."


def split_title_details(value: str) -> tuple[str, str]:
    markers = [
        ". Свидетельство",
        ". Учебное",
        ". Учебник",
        ". Методические",
        ". ISBN",
        ". (Рекомендовано",
        ".(Рекомендовано",
    ]
    for marker in markers:
        index = value.find(marker)
        if index > 0:
            title = value[:index].strip()
            details = value[index + 2 :].strip()
            return title, details
    return value.strip(), ""


def split_citation_parts(citation: str) -> dict[str, str]:
    main, separator, source = citation.partition(" // ")
    if separator:
        split_at = main.rfind(". ")
        if split_at > 0:
            authors = clean_spaces(main[: split_at + 1]).rstrip(",")
            if re.search(r"[a-zа-яё]\.$", authors):
                authors = authors[:-1]
            return {
                "authors": authors,
                "title": clean_spaces(main[split_at + 2 :]).strip(" ."),
                "details": clean_spaces(source),
                "year": extract_year(citation),
            }

    author_token = (
        r"(?:[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё’`-]+(?:\s+[A-ZА-ЯЁ]\.){1,2}"
        r"|(?:[A-ZА-ЯЁ]\.\s*){1,2}[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё’`-]+)"
    )
    author_match = re.match(
        rf"^((?:{author_token})(?:,\s*(?:{author_token}))*)(?:\.\s+|\s+)(.+)$",
        main.strip(),
    )

    if author_match:
        authors = author_match.group(1).strip().rstrip(",")
        title_source = author_match.group(2).strip()
    else:
        authors = "Антамошкин О. А."
        title_source = main.strip()

    if separator:
        title = title_source.strip().rstrip(".")
        details = source.strip()
    else:
        title, details = split_title_details(title_source)

    return {
        "authors": clean_spaces(authors),
        "title": clean_spaces(title).strip(" ."),
        "details": clean_spaces(details),
        "year": extract_year(citation),
    }


def bibtex_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def citation_key(publication: dict[str, str]) -> str:
    year = publication["year"] if publication["year"] != "n.d." else "nd"
    return f"antamoshkin{year}_{int(publication['number']):03d}"


def make_citations(publication: dict[str, str]) -> dict[str, str]:
    citation = publication["gost"]
    parts = split_citation_parts(citation)
    authors = parts["authors"]
    authors_sentence = ensure_period(authors)
    title = parts["title"]
    details = parts["details"]
    year = parts["year"]
    details_sentence = ensure_period(details) if details else ""

    citations = {
        "gost": citation,
        "apa": clean_spaces(
            f"{authors} ({year}). {ensure_period(title)} {details_sentence}"
        ),
        "mla": clean_spaces(
            f'{authors_sentence} "{title}." {details_sentence} {year}.'
        ),
        "chicago": clean_spaces(
            f'{authors_sentence} "{title}." {details_sentence} {year}.'
        ),
        "harvard": clean_spaces(
            f"{authors} {year}. {ensure_period(title)} {details_sentence}"
        ),
        "ieee": clean_spaces(
            f"[{publication['number']}] {authors}, \"{title},\" {details_sentence}"
        ),
        "vancouver": clean_spaces(
            f"{authors_sentence} {ensure_period(title)} {details_sentence} {year}."
        ),
    }

    citations["bibtex"] = (
        f"@misc{{{citation_key(publication)},\n"
        f"  author = {{{bibtex_value(authors)}}},\n"
        f"  title = {{{bibtex_value(title)}}},\n"
        f"  year = {{{year}}},\n"
        f"  note = {{{bibtex_value(citation)}}}\n"
        f"}}"
    )
    return citations


def load_publications() -> list[dict[str, str]]:
    publications: list[dict[str, str]] = []
    section = ""

    for raw_line in BIBLIOGRAPHY_SOURCE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            section = heading.group(1)
            continue

        entry = re.match(r"^(\d+)\.\s+(.+)$", line)
        if not entry or section not in SECTION_LABELS:
            continue

        citation = clean_spaces(entry.group(2))
        publication = {
            "number": entry.group(1),
            "section": section,
            "gost": citation,
            "year": extract_year(citation),
        }
        publication["citations"] = make_citations(publication)  # type: ignore[assignment]
        publications.append(publication)

    return publications


def render_style_switcher(lang: str) -> str:
    aria = "Citation style" if lang == "en" else "Стиль цитирования"
    buttons = []
    for style, labels in CITATION_STYLES:
        pressed = "true" if style == "gost" else "false"
        active = " active" if style == "gost" else ""
        buttons.append(
            f'<button type="button" class="style-button{active}" '
            f'data-style="{style}" aria-pressed="{pressed}">'
            f"{html.escape(labels[lang])}</button>"
        )
    return f'<div class="citation-switcher" role="group" aria-label="{aria}">' + "\n".join(buttons) + "</div>"


def render_publications_page(lang: str) -> str:
    publications = load_publications()
    count = len(publications)
    grouped: dict[str, list[dict[str, str]]] = {section: [] for section in SECTION_LABELS}
    for publication in publications:
        grouped[publication["section"]].append(publication)

    if lang == "ru":
        count_word = ru_plural(count, "позиция", "позиции", "позиций")
        intro = (
            f"Полный реестр содержит {count} {count_word} из исходной библиографической "
            "карточки проекта. ГОСТ-версия сохраняет исходную нормализацию; остальные "
            "стили построены автоматически из тех же данных и требуют ручной сверки "
            "перед подачей в журнал, заявку или официальный отчёт."
        )
        source_note = "Источник: локальный файл библиографии по ГОСТу."
    else:
        intro = (
            f"The full register contains {count} items from the local bibliography note. "
            "The GOST view preserves the source normalization; other styles are generated "
            "automatically from the same data and should be manually verified before journal, "
            "grant, or official-report submission."
        )
        source_note = "Source: local GOST bibliography file."

    parts = [
        '<div class="publications-page" data-style="gost">',
        f"<h1>{'Публикации' if lang == 'ru' else 'Publications'}</h1>",
        f"<p>{html.escape(intro)}</p>",
        f'<p class="source-note">{html.escape(source_note)}</p>',
        render_style_switcher(lang),
    ]

    for section, entries in grouped.items():
        if not entries:
            continue
        section_label = SECTION_LABELS[section][lang]
        item_word = "поз." if lang == "ru" else "items"
        parts.append('<section class="publication-group">')
        parts.append(
            f"<h2>{html.escape(section_label)} "
            f'<span class="group-count">{len(entries)} {item_word}</span></h2>'
        )
        parts.append('<ol class="publication-list">')
        for publication in entries:
            citations = publication["citations"]
            parts.append('<li class="publication-item">')
            parts.append(f'<span class="publication-number">{publication["number"]}</span>')
            parts.append('<div class="publication-citations">')
            parts.append(
                f'<div class="publication-meta">{html.escape(publication["year"])} · '
                f"{html.escape(section_label)}</div>"
            )
            for style, _labels in CITATION_STYLES:
                citation = citations[style]
                if style == "bibtex":
                    parts.append(
                        f'<pre class="citation citation-bibtex" data-citation-style="{style}">'
                        f"<code>{html.escape(citation)}</code></pre>"
                    )
                else:
                    parts.append(
                        f'<p class="citation citation-{style}" data-citation-style="{style}">'
                        f"{html.escape(citation)}</p>"
                    )
            parts.append("</div>")
            parts.append("</li>")
        parts.append("</ol>")
        parts.append("</section>")

    parts.append(
        """<script>
(() => {
  const root = document.querySelector(".publications-page");
  if (!root) return;
  const buttons = Array.from(root.querySelectorAll(".style-button"));
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const style = button.dataset.style;
      root.dataset.style = style;
      buttons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", active ? "true" : "false");
      });
    });
  });
})();
</script>"""
    )
    parts.append("</div>")
    return "\n".join(parts)


def render_nav(lang: str, current_slug: str) -> str:
    links = []
    for slug, labels in PAGES:
        class_name = "active" if slug == current_slug else ""
        links.append(
            f'<a class="{class_name}" href="{page_href(slug)}">{html.escape(labels[lang])}</a>'
        )
    return "\n".join(links)


def render_page(lang: str, slug: str, title: str, body: str) -> str:
    meta = LANG_META[lang]
    other = meta["other"]
    other_href = f"../{other}/{page_href(slug)}"
    nav = render_nav(lang, slug)
    return f"""<!doctype html>
<html lang="{meta["html_lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | {html.escape(meta["site"])}</title>
  <meta name="description" content="{html.escape(meta["site"])} - public profile">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <a class="skip-link" href="#content">{html.escape(meta["skip"])}</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="{html.escape(meta["site"])}">O.A.</a>
      <span>{html.escape(meta["role"])}</span>
    </div>
    <nav class="site-nav" aria-label="Primary navigation">
      {nav}
    </nav>
    <a class="language-link" href="{other_href}">{LANG_META[other]["name"]}</a>
  </header>
  <main id="content" class="content page-{slug}">
    {body}
  </main>
  <footer class="site-footer">
    <span>{html.escape(meta["footer"])}</span>
  </footer>
</body>
</html>
"""


def render_root() -> str:
    return """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Oleslav Antamoshkin</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main class="language-gate">
    <p class="gate-kicker">Personal profile</p>
    <h1>Oleslav Antamoshkin</h1>
    <p>Software engineering · AI · distributed systems</p>
    <div class="gate-links" aria-label="Language selection">
      <a href="ru/index.html">Русская версия</a>
      <a href="en/index.html">English version</a>
    </div>
  </main>
</body>
</html>
"""


def build() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / "ru").mkdir(exist_ok=True)
    (PUBLIC_DIR / "en").mkdir(exist_ok=True)

    for lang in LANG_META:
        for slug, labels in PAGES:
            if slug == "publications":
                title = labels[lang]
                body = render_publications_page(lang)
            else:
                source = CONTENT_DIR / lang / f"{slug}.md"
                markdown = source.read_text(encoding="utf-8")
                title = first_heading(markdown, labels[lang])
                body = markdown_to_html(markdown)
            destination = PUBLIC_DIR / lang / page_href(slug)
            destination.write_text(render_page(lang, slug, title, body), encoding="utf-8")

    (PUBLIC_DIR / "index.html").write_text(render_root(), encoding="utf-8")


if __name__ == "__main__":
    build()
