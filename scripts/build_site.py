from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = ROOT.parent
CONTENT_DIR = ROOT / "content"
PUBLIC_DIR = ROOT / "public"
BIBLIOGRAPHY_SOURCE = WORKSPACE_ROOT / "tmp" / "Bibliography - Oleslav Antamoshkin - GOST.md"
PDF_EXPORT_DIR = PUBLIC_DIR / "downloads"
SITE_URL = "https://oleslav.com"
OG_IMAGE = "og-image.svg"

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

SELECTED_PUBLICATION_NUMBERS = [
    "127",
    "113",
    "114",
    "101",
    "106",
    "121",
    "80",
    "122",
    "119",
    "133",
]

PUBLICATION_BADGES = {
    "70": {
        "ru": ["распределённые системы", "моделирование"],
        "en": ["distributed systems", "simulation"],
    },
    "80": {
        "ru": ["Q2", "SJR 2025: 0.233", "городская оценка"],
        "en": ["Q2", "SJR 2025: 0.233", "city evaluation"],
    },
    "99": {
        "ru": ["распределённые системы", "нейросетевое управление"],
        "en": ["distributed systems", "neural control"],
    },
    "100": {
        "ru": ["распределённые вычисления", "моделирование"],
        "en": ["distributed computing", "modeling"],
    },
    "101": {
        "ru": ["Q2", "SJR 0.40+", "горная промышленность"],
        "en": ["Q2", "SJR 0.40+", "mining"],
    },
    "102": {
        "ru": ["БАС", "YOLO", "компьютерное зрение"],
        "en": ["UAV", "YOLO", "computer vision"],
    },
    "103": {
        "ru": ["3D-реконструкция", "U-Net", "сегментация"],
        "en": ["3D reconstruction", "U-Net", "segmentation"],
    },
    "106": {
        "ru": ["Scopus Q2", "SJR 0.273", "Сибириана"],
        "en": ["Scopus Q2", "SJR 0.273", "Siberiana"],
    },
    "107": {
        "ru": ["БАС", "сенсорные данные"],
        "en": ["UAV", "sensor fusion"],
    },
    "109": {
        "ru": ["бортовой ИИ", "обнаружение объектов"],
        "en": ["on-board AI", "object detection"],
    },
    "113": {
        "ru": ["MDPI", "WEVJ", "энергетика", "электротранспорт"],
        "en": ["MDPI", "WEVJ", "energy systems", "electric transport"],
    },
    "114": {
        "ru": ["MDPI", "WEVJ", "зарядка электромобилей", "моделирование"],
        "en": ["MDPI", "WEVJ", "EV charging", "simulation"],
    },
    "119": {
        "ru": ["БАС", "обработка данных"],
        "en": ["UAV", "data processing"],
    },
    "121": {
        "ru": ["Q3", "SJR 0.272-0.322", "биомасса"],
        "en": ["Q3", "SJR 0.272-0.322", "biomass"],
    },
    "122": {
        "ru": ["Q3", "SJR 0.34-0.38", "машинное обучение"],
        "en": ["Q3", "SJR 0.34-0.38", "machine learning"],
    },
    "127": {
        "ru": ["Q1", "SJR 0.626", "устойчивое развитие"],
        "en": ["Q1", "SJR 0.626", "sustainable development"],
    },
    "133": {
        "ru": ["AISEI 2026", "роботизированная сборка"],
        "en": ["AISEI 2026", "robotic assembly"],
    },
    "134": {
        "ru": ["AISEI 2026", "периферийный ИИ", "обнаружение отказов"],
        "en": ["AISEI 2026", "Edge AI", "fault detection"],
    },
}

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
        "role": "Программная инженерия · ИИ · распределённые системы",
        "footer": "© 2026 Олеслав Антамошкин · Персональный академический и научно-технический профиль",
    },
    "en": {
        "html_lang": "en",
        "name": "EN",
        "other": "ru",
        "skip": "Skip to content",
        "site": "Oleslav Antamoshkin",
        "role": "Software engineering · AI · distributed systems",
        "footer": "© 2026 Oleslav Antamoshkin · Personal academic and R&D profile",
    },
}

PAGE_DESCRIPTIONS = {
    "ru": {
        "index": "Олеслав Антамошкин: программная инженерия, ИИ-системы, распределённые вычисления и прикладные НИОКР.",
        "projects": "Прикладные платформы, исследовательские репозитории и проектные направления Олеслава Антамошкина.",
        "research": "Научные профили, метрики, диссертационные исследования и исследовательский контур Олеслава Антамошкина.",
        "publications": "Избранные публикации, последние работы, полный архив и PDF-версии библиографии в разных стилях.",
        "experience": "Академические должности, проектные роли, компетенции, образование и профессиональное развитие.",
        "contacts": "Электронная почта и публичные профили Олеслава Антамошкина: GitHub, ORCID, Scopus, ResearchGate и СФУ.",
    },
    "en": {
        "index": "Oleslav Antamoshkin: software engineering, AI systems, distributed computing, and applied R&D.",
        "projects": "Applied platforms, research engineering repositories, and project directions by Oleslav Antamoshkin.",
        "research": "Scholarly profiles, metrics, dissertation research, and research context for Oleslav Antamoshkin.",
        "publications": "Selected publications, recent works, full bibliography, and PDF exports in multiple citation styles.",
        "experience": "Academic roles, project leadership, competencies, education, and professional development.",
        "contacts": "Email and public profiles for Oleslav Antamoshkin: GitHub, ORCID, Scopus, ResearchGate, and SFU.",
    },
}


def page_href(slug: str) -> str:
    return "index.html" if slug == "index" else f"{slug}.html"


def site_url(path: str = "") -> str:
    suffix = path.strip("/")
    return SITE_URL if not suffix else f"{SITE_URL}/{suffix}"


def alternate_links(slug: str | None = None) -> str:
    if slug is None:
        targets = [
            ("en", page_path("en", "index")),
            ("ru", page_path("ru", "index")),
            ("x-default", ""),
        ]
    else:
        targets = [
            ("en", page_path("en", slug)),
            ("ru", page_path("ru", slug)),
            ("x-default", ""),
        ]
    return "\n".join(
        f'  <link rel="alternate" hreflang="{hreflang}" href="{html.escape(site_url(path), quote=True)}">'
        for hreflang, path in targets
    )


def page_path(lang: str, slug: str) -> str:
    return f"{lang}/{page_href(slug)}"


def page_description(lang: str, slug: str) -> str:
    return PAGE_DESCRIPTIONS[lang][slug]


def json_script(data: dict[str, object]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{payload}</script>'


def breadcrumb_entries(lang: str, slug: str, title: str) -> list[tuple[str, str]]:
    if lang == "ru":
        entries = [("Профиль", "../index.html"), ("Русская версия", "index.html")]
    else:
        entries = [("Profile", "../index.html"), ("English version", "index.html")]
    if slug != "index":
        entries.append((title, page_href(slug)))
    return entries


def render_breadcrumbs(lang: str, slug: str, title: str) -> str:
    label = "Хлебные крошки" if lang == "ru" else "Breadcrumb"
    entries = breadcrumb_entries(lang, slug, title)
    parts = [f'<nav class="breadcrumbs" aria-label="{html.escape(label)}"><ol>']
    for index, (name, href) in enumerate(entries):
        if index == len(entries) - 1:
            parts.append(f'<li aria-current="page">{html.escape(name)}</li>')
        else:
            parts.append(f'<li><a href="{html.escape(href, quote=True)}">{html.escape(name)}</a></li>')
    parts.append("</ol></nav>")
    return "\n".join(parts)


def breadcrumb_json_ld(lang: str, slug: str, title: str) -> dict[str, object]:
    entries = breadcrumb_entries(lang, slug, title)
    items = []
    for index, (name, _href) in enumerate(entries, start=1):
        if index == 1:
            item_url = site_url()
        elif index == 2:
            item_url = site_url(page_path(lang, "index"))
        else:
            item_url = site_url(page_path(lang, slug))
        items.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": item_url,
            }
        )
    return {"@type": "BreadcrumbList", "itemListElement": items}


def page_json_ld(lang: str, slug: str, title: str, description: str) -> str:
    page_url = site_url(page_path(lang, slug))
    language = LANG_META[lang]["html_lang"]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": site_url("#person"),
                "name": "Oleslav Antamoshkin",
                "alternateName": "Олеслав Александрович Антамошкин",
                "url": site_url(),
                "sameAs": [
                    "https://github.com/oleslav24",
                    "https://orcid.org/0000-0002-5976-5847",
                    "https://www.researchgate.net/profile/Oleslav-Antamoshkin",
                    "https://www.scopus.com/authid/detail.uri?authorId=56825984000",
                ],
            },
            {
                "@type": "WebSite",
                "@id": site_url("#website"),
                "url": site_url(),
                "name": "Oleslav Antamoshkin",
                "inLanguage": language,
            },
            {
                "@type": "Article",
                "@id": f"{page_url}#article",
                "headline": title,
                "description": description,
                "author": {"@id": site_url("#person")},
                "mainEntityOfPage": page_url,
                "inLanguage": language,
                "dateModified": "2026-07-07",
            },
            breadcrumb_json_ld(lang, slug, title),
        ],
    }
    return json_script(data)


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

        if stripped.startswith("<") and stripped.endswith(">"):
            flush_paragraph()
            close_list()
            output.append(stripped)
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

    if not BIBLIOGRAPHY_SOURCE.exists():
        return publications

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


def publication_sort_key(publication: dict[str, str]) -> int:
    return int(publication["number"])


def publication_tags(publication: dict[str, str], lang: str) -> list[str]:
    tags = PUBLICATION_BADGES.get(publication["number"], {})
    return tags.get(lang, [])


def render_publication_item(
    publication: dict[str, str],
    lang: str,
    show_number: bool = True,
) -> str:
    section_label = SECTION_LABELS[publication["section"]][lang]
    citations = publication["citations"]
    class_name = "publication-item" if show_number else "publication-item publication-item-no-number"
    parts = [f'<li class="{class_name}">']
    if show_number:
        parts.append(f'<span class="publication-number">{publication["number"]}</span>')
    parts.append('<div class="publication-citations">')
    parts.append(
        f'<div class="publication-meta">{html.escape(publication["year"])} · '
        f"{html.escape(section_label)}</div>"
    )

    tags = publication_tags(publication, lang)
    if tags:
        parts.append('<div class="publication-badges">')
        for tag in tags:
            parts.append(f'<span>{html.escape(tag)}</span>')
        parts.append("</div>")

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
    return "\n".join(parts)


def render_publication_section(
    title: str,
    intro: str,
    entries: list[dict[str, str]],
    lang: str,
    class_name: str,
    show_numbers: bool = True,
) -> str:
    if lang == "ru" and class_name == "publication-selected":
        item_word = "работ"
    elif lang == "ru" and class_name == "publication-recent":
        item_word = "публикаций"
    else:
        item_word = "поз." if lang == "ru" else "items"
    parts = [f'<section class="publication-group {class_name}">']
    parts.append(
        f"<h2>{html.escape(title)} "
        f'<span class="group-count">{len(entries)} {item_word}</span></h2>'
    )
    if intro:
        parts.append(f'<p class="publication-section-intro">{html.escape(intro)}</p>')
    parts.append('<ol class="publication-list">')
    for publication in entries:
        parts.append(render_publication_item(publication, lang, show_numbers))
    parts.append("</ol>")
    parts.append("</section>")
    return "\n".join(parts)


def render_publication_downloads(lang: str) -> str:
    if lang == "ru":
        title = "PDF-версии"
        intro = "Готовые списки публикаций для пересылки, заявок и рабочих материалов."
    else:
        title = "PDF versions"
        intro = "Ready-to-share publication lists for applications and working materials."

    links = []
    for style, labels in CITATION_STYLES:
        href = f"../downloads/publications-{style}.pdf"
        links.append(
            f'<a href="{href}" target="_blank" rel="noreferrer">'
            f"{html.escape(labels[lang])} PDF</a>"
        )

    return (
        '<section class="publication-downloads" aria-label="PDF downloads">'
        f'<p class="section-kicker">{html.escape(title)}</p>'
        f"<p>{html.escape(intro)}</p>"
        '<div class="publication-download-links">'
        + "\n".join(links)
        + "</div></section>"
    )


def render_citation_tools(lang: str) -> str:
    if lang == "ru":
        summary = "Форматы цитирования"
        note = (
            "По умолчанию показан ГОСТ. Остальные стили генерируются автоматически "
            "из той же записи и требуют ручной сверки перед официальной подачей."
        )
    else:
        summary = "Citation formats"
        note = (
            "GOST is shown by default. Other styles are generated automatically "
            "from the same source record and should be checked before official use."
        )

    return (
        '<details class="citation-tools">'
        f"<summary>{html.escape(summary)}</summary>"
        f"<p>{html.escape(note)}</p>"
        f"{render_style_switcher(lang)}"
        "</details>"
    )


def render_publications_page(lang: str) -> str:
    publications = load_publications()
    count = len(publications)
    grouped: dict[str, list[dict[str, str]]] = {section: [] for section in SECTION_LABELS}
    for publication in publications:
        grouped[publication["section"]].append(publication)

    by_number = {publication["number"]: publication for publication in publications}
    selected = [
        by_number[number]
        for number in SELECTED_PUBLICATION_NUMBERS
        if number in by_number
    ]
    research_section = next(iter(SECTION_LABELS))
    recent = sorted(
        grouped[research_section],
        key=publication_sort_key,
        reverse=True,
    )[:10]

    if lang == "ru":
        count_word = ru_plural(count, "позиция", "позиции", "позиций")
        intro = (
            "Публичный раздел публикаций: наверху избранные работы и свежие записи, "
            "ниже полный архив с переключением стилей цитирования. PDF-версии "
            f"доступны отдельными файлами; всего в архиве {count} {count_word}."
        )
        selected_title = "Избранные публикации"
        selected_intro = (
            "Короткий список значимых работ: журнальные публикации Q1-Q3, "
            "MDPI / World Electric Vehicle Journal, «Сибириана», БАС "
            "и AISEI 2026."
        )
        recent_title = "Последние публикации"
        recent_intro = "Десять последних научных публикаций."
        archive_summary = f"Полная библиография - {count} {count_word}"
    else:
        intro = (
            "A public publication section: selected and recent works first, followed "
            f"by the full bibliography with citation style switching. PDF versions "
            f"are available as separate files; the archive contains {count} items."
        )
        selected_title = "Selected publications"
        selected_intro = (
            "A short list of significant works: Q1-Q3 journal publications, "
            "MDPI / World Electric Vehicle Journal, Siberiana, UAV systems, "
            "and AISEI 2026."
        )
        recent_title = "Recent publications"
        recent_intro = "The ten latest research publications."
        archive_summary = f"Full bibliography - {count} items"

    parts = [
        '<div class="publications-page" data-style="gost">',
        f"<h1>{'Публикации' if lang == 'ru' else 'Publications'}</h1>",
        f"<p>{html.escape(intro)}</p>",
        render_publication_downloads(lang),
        render_publication_section(
            selected_title,
            selected_intro,
            selected,
            lang,
            "publication-selected",
            show_numbers=False,
        ),
        render_publication_section(recent_title, recent_intro, recent, lang, "publication-recent"),
        render_citation_tools(lang),
        '<details class="bibliography-archive">',
        f"<summary>{html.escape(archive_summary)}</summary>",
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
            parts.append(render_publication_item(publication, lang))
        parts.append("</ol>")
        parts.append("</section>")

    parts.append("</details>")
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


def pdf_font_path() -> Path | None:
    candidates = [
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def build_publication_pdf_exports() -> None:
    if not BIBLIOGRAPHY_SOURCE.exists():
        return

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate
    except ImportError:
        return

    font_path = pdf_font_path()
    if font_path is None:
        return

    publications = load_publications()
    PDF_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    font_name = "SiteSans"
    if font_name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))

    title_style = ParagraphStyle(
        "Title",
        fontName=font_name,
        fontSize=15,
        leading=19,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName=font_name,
        fontSize=8.5,
        leading=11.5,
        spaceAfter=7,
        wordWrap="CJK",
    )
    code_style = ParagraphStyle(
        "Code",
        fontName=font_name,
        fontSize=7,
        leading=9,
        spaceAfter=7,
    )

    def page_footer(canvas, document) -> None:
        canvas.saveState()
        canvas.setFont(font_name, 8)
        canvas.setFillColor(colors.HexColor("#606060"))
        canvas.drawRightString(190 * mm, 10 * mm, str(document.page))
        canvas.restoreState()

    for style, labels in CITATION_STYLES:
        destination = PDF_EXPORT_DIR / f"publications-{style}.pdf"
        document = SimpleDocTemplate(
            str(destination),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
            title=f"Oleslav Antamoshkin - Publications - {labels['en']}",
        )
        story = [
            Paragraph(
                f"Oleslav Antamoshkin - Publications - {html.escape(labels['en'])}",
                title_style,
            )
        ]

        for publication in publications:
            citation = publication["citations"][style]
            if style == "bibtex":
                story.append(Preformatted(citation, code_style))
            else:
                story.append(
                    Paragraph(
                        f"{publication['number']}. {html.escape(citation)}",
                        body_style,
                    )
                )

        document.build(story, onFirstPage=page_footer, onLaterPages=page_footer)


def render_nav(lang: str, current_slug: str) -> str:
    links = []
    for slug, labels in PAGES:
        class_name = "active" if slug == current_slug else ""
        current = ' aria-current="page"' if slug == current_slug else ""
        links.append(
            f'<a class="{class_name}" href="{page_href(slug)}"{current}>{html.escape(labels[lang])}</a>'
        )
    return "\n".join(links)


def render_page(lang: str, slug: str, title: str, body: str) -> str:
    meta = LANG_META[lang]
    other = meta["other"]
    other_href = f"../{other}/{page_href(slug)}"
    nav = render_nav(lang, slug)
    description = page_description(lang, slug)
    url = site_url(page_path(lang, slug))
    og_locale = "ru_RU" if lang == "ru" else "en_US"
    breadcrumbs = render_breadcrumbs(lang, slug, title)
    json_ld = page_json_ld(lang, slug, title, description)
    return f"""<!doctype html>
<html lang="{meta["html_lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | {html.escape(meta["site"])}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{html.escape(url, quote=True)}">
{alternate_links(slug)}
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:title" content="{html.escape(title)} | {html.escape(meta["site"])}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{html.escape(url, quote=True)}">
  <meta property="og:image" content="{html.escape(site_url(OG_IMAGE), quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)} | {html.escape(meta["site"])}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{html.escape(site_url(OG_IMAGE), quote=True)}">
  <link rel="stylesheet" href="../styles.css">
  {json_ld}
</head>
<body>
  <a class="skip-link" href="#content">{html.escape(meta["skip"])}</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="{html.escape(meta["site"])}">OA</a>
      <span>{html.escape(meta["role"])}</span>
    </div>
    <nav class="site-nav" aria-label="Primary navigation">
      {nav}
    </nav>
    <a class="language-link" href="{other_href}">{LANG_META[other]["name"]}</a>
  </header>
  <main id="content" class="content page-{slug}">
    {breadcrumbs}
    {body}
  </main>
  <footer class="site-footer">
    <span>{html.escape(meta["footer"])}</span>
  </footer>
</body>
</html>
"""


def root_json_ld() -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": site_url("#person"),
                "name": "Oleslav Antamoshkin",
                "alternateName": "Олеслав Александрович Антамошкин",
                "url": site_url(),
                "sameAs": [
                    "https://github.com/oleslav24",
                    "https://orcid.org/0000-0002-5976-5847",
                    "https://www.researchgate.net/profile/Oleslav-Antamoshkin",
                    "https://www.scopus.com/authid/detail.uri?authorId=56825984000",
                ],
            },
            {
                "@type": "WebSite",
                "@id": site_url("#website"),
                "url": site_url(),
                "name": "Oleslav Antamoshkin",
                "inLanguage": ["ru", "en"],
            },
            {
                "@type": "Article",
                "@id": site_url("#article"),
                "headline": "Oleslav Antamoshkin",
                "description": "Personal academic and applied R&D profile of Oleslav Antamoshkin.",
                "author": {"@id": site_url("#person")},
                "mainEntityOfPage": site_url(),
                "inLanguage": ["ru", "en"],
                "dateModified": "2026-07-07",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Oleslav Antamoshkin",
                        "item": site_url(),
                    }
                ],
            },
        ],
    }
    return json_script(data)


def render_root() -> str:
    description = (
        "Олеслав Антамошкин: программная инженерия, ИИ-системы, "
        "распределённые вычисления, мониторинг по данным БАС и прикладные НИОКР."
    )
    return """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Олеслав Александрович Антамошкин</title>
  <meta name="description" content="{description}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{url}">
{alternate}
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="Олеслав Александрович Антамошкин">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Олеслав Александрович Антамошкин">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">
  <link rel="stylesheet" href="styles.css">
  {json_ld}
</head>
<body>
  <a class="skip-link" href="#content">К содержанию</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="Олеслав Антамошкин" aria-current="page">ОА</a>
      <span>Программная инженерия · ИИ · распределённые системы</span>
    </div>
    <nav class="site-nav" aria-label="Основная навигация">
      <a class="active" href="index.html" aria-current="page">Главная</a>
      <a href="ru/projects.html">Проекты</a>
      <a href="ru/research.html">Исследования</a>
      <a href="ru/publications.html">Публикации</a>
      <a href="ru/experience.html">Роли</a>
      <a href="ru/contacts.html">Контакты</a>
    </nav>
    <a class="language-link" href="en/index.html">EN</a>
  </header>
  <main id="content" class="content page-root">
    <nav class="breadcrumbs" aria-label="Хлебные крошки">
      <ol>
        <li aria-current="page">Профиль</li>
      </ol>
    </nav>
    <h1>Олеслав Александрович Антамошкин</h1>
    <p>Программная инженерия · ИИ-системы · прикладные НИОКР</p>
    <p>Доктор технических наук; заведующий кафедрой программной инженерии ИКИТ Сибирского федерального университета; профессор кафедры информационных технологий в креативных и культурных индустриях ГИ СФУ.</p>
    <p>Руковожу исследовательскими и инженерными проектами в области распределённых систем, компьютерного зрения, мониторинга на основе данных БАС, цифровых платформ и ИИ-инструментов для программной инженерии.</p>
    <div class="gate-links" aria-label="Основные разделы">
      <a href="ru/projects.html">Проекты</a>
      <a href="ru/publications.html">Публикации</a>
      <a href="ru/contacts.html">Контакты</a>
    </div>
  </main>
  <footer class="site-footer">
    <span>© 2026 Олеслав Антамошкин · Персональный академический и научно-технический профиль</span>
  </footer>
</body>
</html>
""".format(
        description=html.escape(description),
        url=html.escape(site_url(), quote=True),
        image=html.escape(site_url(OG_IMAGE), quote=True),
        alternate=alternate_links(),
        json_ld=root_json_ld(),
    )


def render_sitemap() -> str:
    urls = [("", "1.0")]
    for lang in ("en", "ru"):
        for slug, _labels in PAGES:
            urls.append((page_path(lang, slug), "0.8" if slug != "index" else "0.9"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(site_url(path))}</loc>")
        lines.append("    <lastmod>2026-07-07</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def render_robots() -> str:
    return f"""User-agent: *
Allow: /

Sitemap: {site_url("sitemap.xml")}
"""


def render_favicon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img" aria-labelledby="title">
  <title id="title">Oleslav Antamoshkin</title>
  <rect width="64" height="64" fill="#111111"/>
  <text x="32" y="40" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="700" text-anchor="middle">OA</text>
</svg>
"""


def render_og_image() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
  <title id="title">Oleslav Antamoshkin</title>
  <desc id="desc">Personal academic and applied R&amp;D profile</desc>
  <rect width="1200" height="630" fill="#ffffff"/>
  <rect x="72" y="72" width="220" height="220" fill="#111111"/>
  <text x="182" y="218" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="92" font-weight="700" text-anchor="middle">OA</text>
  <text x="72" y="390" fill="#111111" font-family="Arial, Helvetica, sans-serif" font-size="64" font-weight="700">Oleslav Antamoshkin</text>
  <text x="72" y="455" fill="#606060" font-family="Arial, Helvetica, sans-serif" font-size="32">Software engineering, AI systems, applied R&amp;D</text>
  <line x1="72" y1="508" x2="1128" y2="508" stroke="#d8d8d8" stroke-width="2"/>
  <text x="72" y="560" fill="#606060" font-family="Arial, Helvetica, sans-serif" font-size="24">Siberian Federal University · Distributed systems · UAV-based monitoring</text>
</svg>
"""


def render_404() -> str:
    description = "Page not found. Choose the Russian or English version of the personal profile site."
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found | Oleslav Antamoshkin</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{url}">
{alternate}
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="Oleslav Antamoshkin">OA</a>
      <span>Software engineering · AI · distributed systems</span>
    </div>
    <nav class="site-nav" aria-label="Primary navigation">
      <a href="ru/index.html">Главная</a>
      <a href="en/index.html">Home</a>
      <a href="ru/projects.html">Проекты</a>
      <a href="en/publications.html">Publications</a>
      <a href="en/contacts.html">Contact</a>
    </nav>
  </header>
  <main id="content" class="content page-404">
    <h1>Page not found</h1>
    <p>The requested page is unavailable. Use one of the links below to return to the site.</p>
    <div class="gate-links" aria-label="Site sections">
      <a href="ru/index.html">Русская версия</a>
      <a href="en/index.html">English version</a>
      <a href="ru/contacts.html">Контакты</a>
      <a href="en/contacts.html">Contact</a>
    </div>
  </main>
  <footer class="site-footer">
    <span>© 2026 Oleslav Antamoshkin · Personal academic and R&D profile</span>
  </footer>
</body>
</html>
""".format(
        description=html.escape(description),
        url=html.escape(site_url("404.html"), quote=True),
        alternate=alternate_links(),
    )


def build() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    (PUBLIC_DIR / "ru").mkdir(exist_ok=True)
    (PUBLIC_DIR / "en").mkdir(exist_ok=True)
    bibliography_available = BIBLIOGRAPHY_SOURCE.exists()

    for lang in LANG_META:
        for slug, labels in PAGES:
            destination = PUBLIC_DIR / lang / page_href(slug)
            if slug == "publications":
                if not bibliography_available and destination.exists():
                    print(
                        f"Warning: bibliography source not found at {BIBLIOGRAPHY_SOURCE}; "
                        f"preserving {destination}."
                    )
                    continue
                title = labels[lang]
                body = render_publications_page(lang)
            else:
                source = CONTENT_DIR / lang / f"{slug}.md"
                markdown = source.read_text(encoding="utf-8")
                title = first_heading(markdown, labels[lang])
                body = markdown_to_html(markdown)
            destination.write_text(render_page(lang, slug, title, body), encoding="utf-8")

    (PUBLIC_DIR / "index.html").write_text(render_root(), encoding="utf-8")
    (PUBLIC_DIR / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")
    (PUBLIC_DIR / "robots.txt").write_text(render_robots(), encoding="utf-8")
    (PUBLIC_DIR / "favicon.svg").write_text(render_favicon(), encoding="utf-8")
    (PUBLIC_DIR / OG_IMAGE).write_text(render_og_image(), encoding="utf-8")
    (PUBLIC_DIR / "404.html").write_text(render_404(), encoding="utf-8")
    build_publication_pdf_exports()


if __name__ == "__main__":
    build()
