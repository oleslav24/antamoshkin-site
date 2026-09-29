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
PUBLICATION_EN_TRANSLATIONS = CONTENT_DIR / "en" / "publications.json"
PDF_EXPORT_DIR = PUBLIC_DIR / "downloads"
SITE_URL = "https://oleslav.com"
OG_IMAGE = "og-image.svg"
ASSET_VERSION = "20260929-geo"
PERSON_ID = "https://oleslav.com/#oleslav-antamoshkin"
BUILD_DATE = "2026-09-29"
INDEXNOW_KEY = "4f8b0c59e8194679b2af098c4d7e3a91"

HOMEPAGE_TITLES = {
    "en": "Oleslav Antamoshkin — Software & AI Architect",
    "ru": "Олеслав Антамошкин — архитектор программных и AI-систем",
}

PAGES = [
    ("index", {"ru": "Главная", "en": "Home"}),
    ("projects", {"ru": "Проекты", "en": "Projects"}),
    ("experience", {"ru": "Опыт", "en": "Experience"}),
    ("research", {"ru": "Исследования", "en": "Research"}),
    ("publications", {"ru": "Публикации", "en": "Publications"}),
    ("contacts", {"ru": "Контакты", "en": "Contact"}),
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
    "186",
    "127",
    "113",
    "114",
    "101",
    "106",
    "80",
    "122",
    "119",
    "133",
]

PUBLICATION_BADGES = {
    "186": {
        "ru": ["Scientific Reports", "Scopus Q1", "БАС", "компьютерное зрение"],
        "en": ["Scientific Reports", "Scopus Q1", "UAV", "computer vision"],
    },
    "70": {
        "ru": ["распределённые системы", "моделирование"],
        "en": ["distributed systems", "simulation"],
    },
    "80": {
        "ru": ["Scopus Q2", "SJR 2025: 0.233", "городская оценка"],
        "en": ["Scopus Q2", "SJR 2025: 0.233", "city evaluation"],
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
        "ru": ["Scopus Q2", "SJR 0.40+", "горная промышленность"],
        "en": ["Scopus Q2", "SJR 0.40+", "mining"],
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
        "ru": ["MDPI", "WEVJ", "Scopus Q2", "энергетика", "электротранспорт"],
        "en": ["MDPI", "WEVJ", "Scopus Q2", "energy systems", "electric transport"],
    },
    "114": {
        "ru": ["MDPI", "WEVJ", "Scopus Q2", "зарядка электромобилей", "моделирование"],
        "en": ["MDPI", "WEVJ", "Scopus Q2", "EV charging", "simulation"],
    },
    "119": {
        "ru": ["БАС", "обработка данных"],
        "en": ["UAV", "data processing"],
    },
    "121": {
        "ru": ["Scopus Q3", "SJR 0.272-0.322", "биомасса"],
        "en": ["Scopus Q3", "SJR 0.272-0.322", "biomass"],
    },
    "122": {
        "ru": ["Scopus Q3", "SJR 0.34-0.38", "машинное обучение"],
        "en": ["Scopus Q3", "SJR 0.34-0.38", "machine learning"],
    },
    "127": {
        "ru": ["Scopus Q1", "SJR 0.626", "устойчивое развитие"],
        "en": ["Scopus Q1", "SJR 0.626", "sustainable development"],
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

PUBLICATION_LOCALIZED_AUTHORS = {
    "80": {
        "ru": "Антамошкин О. А., Ступина А., Шагаева О., Ямалетдинов С., Кузьмич Р., Руига И.",
        "en": "Antamoshkin O. A., Stupina A., Shagaeva O., Yamaletdinov S., Kuzmich R., Ruiga I.",
    },
    "101": {
        "ru": "Антамошкин О. А., Панфилов И. А., Федорова Н. В., Дерюгин Ф. Ф., Бянкин В. Е.",
        "en": "Antamoshkin O. A., Panfilov I. A., Fedorova N. V., Deryugin F. F., Byankin V. E.",
    },
    "106": {
        "ru": "Антамошкин О. А., Сомов А. К., Брюханова Е. Р., Плешкова Т. С.",
        "en": "Antamoshkin O. A., Somov A. K., Bryukhanova E. R., Pleshkova T. S.",
    },
    "113": {
        "ru": "Антамошкин О. А., Малозёмов В. Б., Мартюшев Н. В., Конюхов В. Ю., Матиенко О. И., Кукарцев В. В., Карлина И. Ю.",
        "en": "Antamoshkin O. A., Malozyomov B. V., Martyushev N. V., Konyukhov V. Yu., Matienko O. I., Kukartsev V. V., Karlina Y. I.",
    },
    "114": {
        "ru": "Антамошкин О. А., Хекерт Е. В., Малозёмов В. Б., Клюев В. Р., Мартюшев Н. В., Конюхов В. Ю., Кукарцев В. В., Ремезов И. С.",
        "en": "Antamoshkin O. A., Khekert E. V., Malozyomov B. V., Klyuev R. V., Martyushev N. V., Konyukhov V. Yu., Kukartsev V. V., Remezov I. S.",
    },
    "119": {
        "ru": "Антамошкин О. А., Гулютин Н. Н., Ермиенко Н. А., Кретинин В. В., Труханов Е. В.",
        "en": "Antamoshkin O. A., Gulyutin N. N., Ermienko N. A., Kretinin V. V., Trukhanov E. V.",
    },
    "121": {
        "ru": "Антамошкин О. А., Кузнецова Ю. С., Кадиров К. А., Сергеева Н. В., Малыха Е. Ф.",
        "en": "Antamoshkin O. A., Kuznetsova Y. S., Kadirov K. A., Sergeyeva N. V., Malykha E. F.",
    },
    "122": {
        "ru": "Антамошкин О. А., Красовская Л. В., Тынченко В. С., Пчелинцева С. В., Никаноров М. С.",
        "en": "Antamoshkin O. A., Krasovskaya L. V., Tynchenko V. S., Pchelintseva S. V., Nikanorov M. S.",
    },
    "127": {
        "ru": "Антамошкин О. А., Самарина В. П., Самарин А. В., Дорофеев Е. М.",
        "en": "Antamoshkin O. A., Samarina V. P., Samarin A. V., Dorofeev E. M.",
    },
    "129": {
        "ru": "Li J., Antamoshkin O. A.",
        "en": "Li J., Antamoshkin O. A.",
    },
    "133": {
        "ru": "Антамошкин О. А., Красовская Л. В., Кукарцева О. И., Соловьёва Т. В., Супрун Е. В., Шиверская М.",
        "en": "Antamoshkin O. A., Krasovskaya L. V., Kukartseva O. I., Solovyova T. V., Suprun E. V., Shiverskaia M.",
    },
    "134": {
        "ru": "Антамошкин О. А., Панченко В., Ашмарин Д. Е., Алмазова Е., Кукарцева С. В., Бирюков П. А.",
        "en": "Antamoshkin O. A., Panchenko V., Ashmarin D. E., Almazova E., Kukartseva S. V., Biryukov P. A.",
    },
    "186": {
        "ru": "Малашин В. Ю., Масич А. Ю., Тынченко В. С., Антамошкин О. А., Мартысюк Г. И., Нелюб А. И., Бородулин В. В., Гантимуров А.",
        "en": "Malashin V. Yu., Masich A. Yu., Tynchenko V. S., Antamoshkin O. A., Martysyuk G. I., Nelyub A. I., Borodulin V. V., Gantimurov A.",
    },
    "187": {
        "ru": "Антамошкин О. А., Жучков Ф. Г., Колосова О. В.",
        "en": "Antamoshkin O. A., Zhuchkov F. G., Kolosova O. V.",
    },
    "188": {
        "ru": "Ступина А. А., Антамошкин О. А., Кукарцев В. В., и др",
        "en": "Stupina A. A., Antamoshkin O. A., Kukartsev V. V., et al",
    },
    "189": {
        "ru": "Ступина А. А., Антамошкин О. А., Кукарцев В. В., и др",
        "en": "Stupina A. A., Antamoshkin O. A., Kukartsev V. V., et al",
    },
    "190": {
        "ru": "Антамошкин О. А., Ступина А. А., Кукарцев В. В., и др",
        "en": "Antamoshkin O. A., Stupina A. A., Kukartsev V. V., et al",
    },
    "191": {
        "ru": "Рукша Т. Г., Антамошкин О. А., Михалев А. С. [и др.]",
        "en": "T. G. Ruksha, O. A. Antamoshkin, A. S. Mikhalev et al.",
    },
}

PUBLICATION_AUTHOR_LANGUAGE = {
    "80": "en",
    "101": "ru",
    "106": "en",
    "113": "en",
    "114": "en",
    "119": "ru",
    "121": "en",
    "122": "en",
    "127": "ru",
    "129": "en",
    "133": "en",
    "134": "en",
    "186": "en",
    "187": "ru",
    "188": "ru",
    "189": "ru",
    "190": "ru",
    "191": "ru",
}

PUBLICATION_CANONICAL_PARTS = {
    "106": {
        "title": "Digital Platform of Yenisei Siberia “Siberiana”",
        "details": (
            "In: J. Sib. Fed. Univ. Humanit. Soc. Sci., 2024, 17(9), "
            "1782–1789. EDN: RMZJPT."
        ),
    },
}

PUBLICATION_LOCALIZED_PARTS = {
    "101": {
        "en": {
            "title": "Prevention of Air Pollution During Open-Pit Mining of Ore Deposits",
            "details": (
                "MIAB. Mining Informational and Analytical Bulletin. 2023;(11-1):"
                "252–264. DOI: 10.25018/0236_1493_2023_111_0_252."
            ),
        },
    },
    "119": {
        "en": {
            "title": "Methodology for Improving Data Processing Accuracy in Onboard Unmanned Aerial Systems",
            "details": (
                "Aerospace Instrument Engineering. 2025;(10):11–20. "
                "DOI: 10.25791/aviakosmos.10.2025.1511."
            ),
        },
    },
    "127": {
        "en": {
            "title": (
                "Application of Information Technologies to the Management and "
                "Sustainable Development of Mountain Territories"
            ),
            "details": (
                "Sustainable Development of Mountain Territories. 2025;17(4(66)):"
                "2175–2187. DOI: 10.21177/1998-4502-2025-174-2175-2187."
            ),
        },
    },
    "187": {
        "en": {
            "title": (
                "Algorithm for Managing the Quality of Changes in an Organizational "
                "and Production Process Involving an AI Agent"
            ),
            "details": (
                "Automation in Industry. 2026; No. 7. "
                "URL: https://avtprom.ru/sistemy-upravleniya-biznes-protsessami-1."
            ),
        },
    },
    "129": {
        "en": {
            "title": "Tiered Neighborhood-Exchange Differential Evolution for Budget-Constrained Multi-Root Localization of Nonlinear Equation Systems",
            "details": "Modeling, Optimization and Information Technology. 2026;14(4(55)). DOI: 10.26102/2310-6018/2026.55.4.016. EDN: BTYULL.",
        },
        "ru": {
            "title": "Tiered Neighborhood-Exchange Differential Evolution for Budget-Constrained Multi-Root Localization of Nonlinear Equation Systems",
            "details": "Modeling, Optimization and Information Technology. 2026;14(4(55)). DOI: 10.26102/2310-6018/2026.55.4.016. EDN: BTYULL.",
        },
    },
    "188": {
        "en": {
            "title": "Information Systems Design: Monograph",
            "details": (
                "Moscow: Russian State Agrarian University, 2026. 198 p. "
                "ISBN 978-5-9675-2150-8. EDN UWUDUR."
            ),
        },
    },
    "189": {
        "en": {
            "title": "Software Engineering: Theory and Practice: Study Guide",
            "details": (
                "Moscow: Russian State Agrarian University, 2026. 245 p. "
                "ISBN 978-5-9675-2151-5. EDN EGWPEK."
            ),
        },
    },
    "190": {
        "en": {
            "title": "Decision Support Systems: Textbook",
            "details": "Moscow: Russian State Agrarian University, 2026. 112 p. EDN OJTXFE.",
        },
    },
}


def load_publication_en_translations() -> dict[str, dict[str, str]]:
    if not PUBLICATION_EN_TRANSLATIONS.exists():
        return {}
    try:
        translations = json.loads(PUBLICATION_EN_TRANSLATIONS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(translations, dict):
        return {}
    return {
        number: values
        for number, values in translations.items()
        if isinstance(number, str)
        and isinstance(values, dict)
        and all(isinstance(value, str) for value in values.values())
    }


PUBLICATION_EN_TRANSLATION_DATA = load_publication_en_translations()

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
        "role": "Архитектура ПО · AI-системы · прикладная разработка",
        "footer": "© 2026 Олеслав Антамошкин · Архитектура ПО · AI-системы · Прикладная разработка",
    },
    "en": {
        "html_lang": "en",
        "name": "EN",
        "other": "ru",
        "skip": "Skip to content",
        "site": "Oleslav Antamoshkin",
        "role": "Software Architecture · AI Systems · Applied Engineering",
        "footer": "© 2026 Oleslav Antamoshkin · Software Architecture · AI Systems · Applied Engineering",
    },
}

PAGE_DESCRIPTIONS = {
    "ru": {
        "index": "Архитектор программных и AI-систем: распределённые системы, искусственный интеллект, компьютерное зрение, БАС, цифровые платформы и техническое руководство разработкой.",
        "projects": "Программные и AI-системы, инженерные репозитории и проектные направления Олеслава Антамошкина.",
        "research": "Научные профили, метрики, диссертационные исследования и исследовательский контур Олеслава Антамошкина.",
        "publications": "Избранные публикации, последние работы, полный архив и PDF-версии библиографии в разных стилях.",
        "experience": "Архитектура ПО, техническое руководство, инженерные компетенции, проекты и академический профиль Олеслава Антамошкина.",
        "contacts": "Электронная почта и публичные профили Олеслава Антамошкина: GitHub, ORCID, Scopus, ResearchGate и СФУ.",
        "about": "Профессиональный и научный профиль Олеслава Антамошкина: архитектора программных и AI-систем, доктора технических наук и руководителя инженерных проектов.",
    },
    "en": {
        "index": "Software and AI architect specializing in distributed systems, AI platforms, computer vision, UAV technologies, digital platforms, and engineering leadership.",
        "projects": "Software and AI systems, engineering repositories, and project directions by Oleslav Antamoshkin.",
        "research": "Scholarly profiles, metrics, dissertation research, and research context for Oleslav Antamoshkin.",
        "publications": "Selected publications, recent works, full bibliography, and PDF exports in multiple citation styles.",
        "experience": "Software architecture, technical leadership, engineering competencies, projects, and academic background of Oleslav Antamoshkin.",
        "contacts": "Email and public profiles for Oleslav Antamoshkin: GitHub, ORCID, Scopus, ResearchGate, and SFU.",
        "about": "Professional and research profile of Oleslav Antamoshkin, a Software & AI Architect, Doctor of Engineering Sciences, and engineering project leader.",
    },
}


def page_href(slug: str) -> str:
    return "index.html" if slug == "index" else f"{slug}.html"


def site_url(path: str = "") -> str:
    suffix = path.strip("/")
    return f"{SITE_URL}/" if not suffix else f"{SITE_URL}/{suffix}"


def versioned_asset(path: str) -> str:
    return f"{path}?v={ASSET_VERSION}"


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
    if slug == "publications":
        return f"{lang}/publications"
    return f"{lang}/{page_href(slug)}"


def page_description(lang: str, slug: str) -> str:
    return PAGE_DESCRIPTIONS[lang][slug]


def json_script(data: dict[str, object]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{payload}</script>'


def person_entity() -> dict[str, object]:
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Oleslav Antamoshkin",
        "alternateName": [
            "Oleslav A. Antamoshkin",
            "Олеслав Антамошкин",
            "Олеслав Александрович Антамошкин",
            "Антамошкин Олеслав",
            "O. A. Antamoshkin",
            "Antamoshkin Oleslav",
        ],
        "url": site_url(),
        "image": site_url("assets/profile-portrait-bw-site.webp"),
        "jobTitle": [
            "Software & AI Architect",
            "Head of the Software Engineering Department",
        ],
        "affiliation": {
            "@type": "CollegeOrUniversity",
            "name": "Siberian Federal University",
        },
        "alumniOf": {
            "@type": "Organization",
            "name": "Siberian State Aerospace University",
        },
        "identifier": [
            {"@type": "PropertyValue", "propertyID": "ORCID", "value": "0000-0002-5976-5847"},
            {"@type": "PropertyValue", "propertyID": "Scopus Author ID", "value": "56825984000"},
            {"@type": "PropertyValue", "propertyID": "Web of Science ResearcherID", "value": "Q-7307-2018"},
            {"@type": "PropertyValue", "propertyID": "RSCI Author ID", "value": "501153"},
            {"@type": "PropertyValue", "propertyID": "SPIN", "value": "8429-4720"},
        ],
        "knowsAbout": [
            "Software Architecture", "Artificial Intelligence", "AI Systems",
            "Agentic Software Engineering", "Autonomous AI Agents", "Distributed Systems",
            "Heterogeneous Computing", "Computer Vision", "UAV Systems",
            "Spatial Monitoring", "GIS and Spatial Data", "Edge AI", "Digital Humanities",
        ],
        "sameAs": [
            "https://github.com/oleslav24",
            "https://orcid.org/0000-0002-5976-5847",
            "https://www.researchgate.net/profile/Oleslav-Antamoshkin",
            "https://www.scopus.com/authid/detail.uri?authorId=56825984000",
            "https://www.webofscience.com/wos/author/rid/Q-7307-2018",
            "https://elibrary.ru/author_profile.asp?id=501153",
            "https://sfu.ru/ru/about/people/a21897cb-8d0f-4ca4-9d2f-7e48780280ea?tab=main",
        ],
    }


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
    page_type = "ProfilePage" if slug == "index" else "WebPage"
    page_id_suffix = "profile" if slug == "index" else "webpage"
    data = {
        "@context": "https://schema.org",
        "@graph": [
            person_entity(),
            {
                "@type": "WebSite",
                "@id": site_url("#website"),
                "url": site_url(),
                "name": "Oleslav Antamoshkin",
                "inLanguage": language,
            },
            {
                "@type": page_type,
                "@id": f"{page_url}#{page_id_suffix}",
                "headline": title,
                "description": description,
                "author": {"@id": PERSON_ID},
                "mainEntityOfPage": page_url,
                "inLanguage": language,
                "dateModified": BUILD_DATE,
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
            identity_hosts = (
                "github.com/oleslav24", "orcid.org/0000-0002-5976-5847",
                "researchgate.net/profile/Oleslav-Antamoshkin", "scopus.com/authid/",
                "webofscience.com/wos/author/rid/", "elibrary.ru/author_profile",
                "sfu.ru/ru/about/people/",
            )
            relation = "me noreferrer" if any(host in href for host in identity_hosts) else "noreferrer"
            attrs = f' target="_blank" rel="{relation}"'
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
        et_al_match = re.match(
            r"^(?P<authors>.+?(?:,\s*)?(?:и\s+др\.|et al\.))\s+(?P<title>.+)$",
            main,
        )
        if et_al_match:
            authors = clean_spaces(et_al_match.group("authors")).rstrip(",")
            if re.search(r"[a-zа-яё]\.$", authors):
                authors = authors[:-1]
            return {
                "authors": authors,
                "title": clean_spaces(et_al_match.group("title")).strip(" ."),
                "details": clean_spaces(source),
                "year": extract_year(citation),
            }
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


def canonical_publication_citation(publication: dict[str, str]) -> str:
    citation = publication["gost"]
    source_parts = split_citation_parts(citation)
    canonical_parts = PUBLICATION_CANONICAL_PARTS.get(publication["number"], {})
    for key, value in canonical_parts.items():
        source_value = source_parts[key]
        if source_value and source_value != value:
            citation = citation.replace(source_value, value)
    return citation


def make_citations(publication: dict[str, str]) -> dict[str, str]:
    citation = canonical_publication_citation(publication)
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


def localize_own_name(value: str, lang: str) -> str:
    if lang == "en":
        replacements = (
            ("Антамошкин О. А.", "Antamoshkin O. A."),
            ("Антамошкин, О. А.", "Antamoshkin O. A."),
        )
    else:
        replacements = (
            ("Antamoshkin O. A.", "Антамошкин О. А."),
            ("Antamoshkin, O. A.", "Антамошкин О. А."),
        )
    for source, target in replacements:
        value = value.replace(source, target)
    return value


def publication_author_variant(publication: dict[str, str], lang: str) -> str | None:
    author_lang = "en" if lang == "en" else PUBLICATION_AUTHOR_LANGUAGE.get(
        publication["number"], "ru"
    )
    if not author_lang:
        return None
    return PUBLICATION_LOCALIZED_AUTHORS.get(publication["number"], {}).get(author_lang)


def localize_publication_text(
    publication: dict[str, str], value: str, lang: str
) -> str:
    source_parts = split_citation_parts(publication["gost"])
    localized_parts = localized_publication_parts(publication, lang)
    for key in ("authors", "title", "details"):
        source_value = source_parts[key]
        localized_value = localized_parts[key]
        if source_value and source_value != localized_value:
            value = value.replace(source_value, localized_value)
    return value


def localized_publication_parts(publication: dict[str, str], lang: str) -> dict[str, str]:
    parts = split_citation_parts(publication["gost"])
    localized_authors = publication_author_variant(publication, lang)
    if localized_authors:
        parts["authors"] = localized_authors
    canonical_parts = PUBLICATION_CANONICAL_PARTS.get(publication["number"], {})
    for key, value in canonical_parts.items():
        parts[key] = value
    translated_parts = PUBLICATION_LOCALIZED_PARTS.get(publication["number"], {}).get(
        lang, {}
    )
    for key, value in translated_parts.items():
        parts[key] = value
    if lang == "en":
        for key, value in PUBLICATION_EN_TRANSLATION_DATA.get(
            publication["number"], {}
        ).items():
            parts[key] = value
    return {
        key: value if key in canonical_parts or key in translated_parts
        or key == "authors" and localized_authors
        else localize_own_name(value, lang)
        for key, value in parts.items()
    }


def render_publication_citations(publication: dict[str, str], lang: str) -> list[str]:
    """Render a single canonical citation and the fields needed for client formatting."""
    citation = localize_publication_text(publication, publication["citations"]["gost"], lang)
    fields = localized_publication_parts(publication, lang)
    fields.update({"number": publication["number"], "gost": citation})
    payload = html.escape(json.dumps(fields, ensure_ascii=False), quote=True)
    return [
        f'<p class="citation" data-citation-style="gost" data-bibliography="{payload}">'
        f"{html.escape(citation)}</p>"
    ]


def render_publication_item(
    publication: dict[str, str],
    lang: str,
    show_number: bool = True,
) -> str:
    section_label = SECTION_LABELS[publication["section"]][lang]
    class_name = "publication-item" if show_number else "publication-item publication-item-no-number"
    parts = [f'<li class="{class_name}">']
    if show_number:
        parts.append(f'<span class="publication-number">{publication["number"]}</span>')
    parts.append('<div class="publication-citations">')
    parts.append(
        f'<div class="publication-meta">{html.escape(publication["year"])} · '
        f"{html.escape(section_label)}</div>"
    )

    publication_parts = localized_publication_parts(publication, lang)
    publication_link = publication_page_href(publication, lang)
    title_html = html.escape(publication_parts["title"])
    if publication_link:
        title_html = f'<a href="{publication_link}">{title_html}</a>'
    parts.append(f'<h3 class="publication-title">{title_html}</h3>')

    tags = publication_tags(publication, lang)
    if tags:
        parts.append('<div class="publication-badges">')
        for tag in tags:
            parts.append(f'<span>{html.escape(tag)}</span>')
        parts.append("</div>")

    parts.extend(render_publication_citations(publication, lang))
    parts.append("</div>")
    parts.append("</li>")
    return "\n".join(parts)


def render_selected_publication_item(publication: dict[str, str], lang: str) -> str:
    section_label = SECTION_LABELS[publication["section"]][lang]
    parts_data = localized_publication_parts(publication, lang)
    tags = publication_tags(publication, lang)
    summary = "Цитирование" if lang == "ru" else "Citation"
    parts = ['<li class="publication-item publication-item-no-number publication-featured-card">']
    parts.append('<article class="publication-card">')
    if tags:
        parts.append('<div class="publication-badges">')
        for tag in tags:
            parts.append(f'<span>{html.escape(tag)}</span>')
        parts.append("</div>")
    publication_link = publication_page_href(publication, lang)
    title_html = html.escape(parts_data["title"])
    if publication_link:
        title_html = f'<a href="{publication_link}">{title_html}</a>'
    parts.append(f'<h3 class="publication-title">{title_html}</h3>')
    parts.append(f'<p class="publication-authors">{html.escape(parts_data["authors"])}</p>')
    if parts_data["details"]:
        parts.append(f'<p class="publication-source">{html.escape(parts_data["details"])}</p>')
    parts.append(
        f'<div class="publication-meta publication-card-meta">{html.escape(publication["year"])} · '
        f"{html.escape(section_label)}</div>"
    )
    parts.append('<details class="publication-citation-details">')
    parts.append(f"<summary>{html.escape(summary)}</summary>")
    parts.extend(render_publication_citations(publication, lang))
    parts.append("</details>")
    parts.append("</article>")
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
        if class_name == "publication-selected":
            parts.append(render_selected_publication_item(publication, lang))
        else:
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
  const sentence = (value) => value && /[.!?]$/.test(value) ? value : `${value}.`;
  const formatCitation = (record, style) => {
    const { authors, title, details, year, number, gost } = record;
    if (style === "gost") return gost;
    if (style === "bibtex") return `@misc{antamoshkin${year}_${String(number).padStart(3, "0")},\n  author = {${authors}},\n  title = {${title}},\n  year = {${year}},\n  note = {${gost}}\n}`;
    if (style === "apa") return `${authors} (${year}). ${sentence(title)} ${sentence(details)}`;
    if (style === "harvard") return `${authors} ${year}. ${sentence(title)} ${sentence(details)}`;
    if (style === "ieee") return `[${number}] ${authors}, "${title}," ${sentence(details)}`;
    if (style === "vancouver") return `${sentence(authors)} ${sentence(title)} ${sentence(details)} ${year}.`;
    return `${sentence(authors)} "${title}." ${sentence(details)} ${year}.`;
  };
  const updateCitations = (style) => {
    root.querySelectorAll("[data-bibliography]").forEach((citation) => {
      const record = JSON.parse(citation.dataset.bibliography);
      citation.textContent = formatCitation(record, style);
      citation.dataset.citationStyle = style;
      citation.classList.toggle("citation-bibtex", style === "bibtex");
    });
  };
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const style = button.dataset.style;
      root.dataset.style = style;
      updateCitations(style);
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
    page_title = HOMEPAGE_TITLES[lang] if slug == "index" else f"{title} | {meta['site']}"
    escaped_page_title = html.escape(page_title)
    nav_label = "Основная навигация" if lang == "ru" else "Primary navigation"
    return f"""<!doctype html>
<html lang="{meta["html_lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_page_title}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{html.escape(url, quote=True)}">
{alternate_links(slug)}
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:title" content="{escaped_page_title}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{html.escape(url, quote=True)}">
  <meta property="og:image" content="{html.escape(site_url(OG_IMAGE), quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escaped_page_title}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{html.escape(site_url(OG_IMAGE), quote=True)}">
  <link rel="stylesheet" href="{html.escape(versioned_asset("../styles.css"), quote=True)}">
  {json_ld}
</head>
<body>
  <a class="skip-link" href="#content">{html.escape(meta["skip"])}</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="{html.escape(meta["site"])}">OA</a>
      <span>{html.escape(meta["role"])}</span>
    </div>
    <nav class="site-nav" aria-label="{html.escape(nav_label)}">
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


PROJECT_ENTITIES = {
    "airscope": {
        "en": {
            "title": "AirScope — UAV Spatial Monitoring",
            "description": "AirScope is a UAV-based spatial monitoring platform for construction, infrastructure, industrial objects, and extended assets.",
            "answer": "AirScope is a platform for turning UAV and spatial data into engineering monitoring, control, and analytical workflows. Oleslav Antamoshkin is its scientific and technical lead and contributes product architecture, technical requirements, module decomposition, and implementation coordination.",
            "problem": "Construction and infrastructure monitoring needs a consistent link between field data, the actual condition of an object, project models, and analytical reporting.",
            "approach": "The platform combines UAV data collection, image processing, photogrammetry, 3D reconstruction, point clouds, computer vision, analytics, and web interfaces.",
            "applications": "Construction progress control, infrastructure monitoring, industrial-object monitoring, and extended-asset monitoring.",
            "results": "The project has a platform concept, product architecture, applied scenarios, a software-registration pipeline, and preparation for commercialization. AirBIM is the construction module for comparison with design models and analytical reporting.",
            "external": ("AirBIM", "https://airbim.org/"),
        },
        "ru": {
            "title": "AirScope — пространственный мониторинг по данным БАС",
            "description": "AirScope — платформа дистанционного пространственного мониторинга строительства, инфраструктуры, промышленных объектов и протяжённых активов по данным БАС.",
            "answer": "AirScope — платформа, превращающая данные БАС и пространственные данные в инженерные контуры мониторинга, контроля и аналитики. Олеслав Антамошкин является научно-техническим лидером проекта и отвечает за архитектуру продукта, технические требования, декомпозицию модулей и координацию реализации.",
            "problem": "Для мониторинга строительства и инфраструктуры требуется связать полевые данные, фактическое состояние объекта, проектные модели и аналитическую отчётность.",
            "approach": "Платформа объединяет сбор данных БАС, обработку изображений, фотограмметрию, 3D-реконструкцию, облака точек, компьютерное зрение, аналитику и веб-интерфейсы.",
            "applications": "Контроль хода строительства, мониторинг инфраструктуры, промышленных объектов и протяжённых активов.",
            "results": "Сформированы концепция платформы, архитектура продукта, прикладные сценарии, контур регистрации ПО и подготовка к коммерциализации. AirBIM является строительным модулем для сопоставления с проектной моделью и аналитической отчётности.",
            "external": ("AirBIM", "https://airbim.org/"),
        },
    },
    "siberiana": {
        "en": {
            "title": "Siberiana — Digital Cultural Heritage Platform",
            "description": "Siberiana is an operational digital platform for cultural heritage resources of the Angara-Yenisei region.",
            "answer": "Siberiana is a digital cultural heritage platform for the Angara-Yenisei region. Oleslav Antamoshkin leads the project and its platform architecture, addressing the integration of heterogeneous cultural heritage materials into an operational public system.",
            "problem": "Cultural heritage materials are heterogeneous and need a usable digital environment for access, integration, visualization, and collaboration with external organizations.",
            "approach": "The platform integrates heterogeneous data, GIS, 3D models, digital archives, visualization, and interfaces for external organizations.",
            "applications": "Digital archives, regional cultural heritage access, visualization, and research and public-information workflows.",
            "results": "Siberiana is a working digital platform and registered software system (certificate No. 2023615453, 07 April 2023).",
            "external": ("siberiana.online", "https://siberiana.online/"),
        },
        "ru": {
            "title": "Сибириана — цифровая платформа культурного наследия",
            "description": "«Сибириана» — работающая цифровая платформа культурного наследия Ангаро-Енисейского региона.",
            "answer": "«Сибириана» — цифровая платформа культурного наследия Ангаро-Енисейского региона. Олеслав Антамошкин руководит проектом и архитектурой платформы; она решает задачу интеграции разнородных материалов культурного наследия в работающую публичную систему.",
            "problem": "Разнородным материалам культурного наследия нужна единая цифровая среда для доступа, интеграции, визуализации и взаимодействия с внешними организациями.",
            "approach": "Платформа объединяет интеграцию разнородных данных, ГИС, 3D-модели, цифровые архивы, визуализацию и интерфейсы внешних организаций.",
            "applications": "Цифровые архивы, доступ к региональному культурному наследию, визуализация и исследовательские и публичные информационные сценарии.",
            "results": "«Сибириана» — полноценно работающая цифровая платформа и зарегистрированная программная система, свидетельство № 2023615453 от 07.04.2023.",
            "external": ("siberiana.online", "https://siberiana.online/"),
        },
    },
}

EXPERTISE_ENTITIES = {
    "software-architecture": {
        "en": ("Software Architecture", "Software architecture concerns the structure, interfaces, and evolution of complex software systems. In Oleslav Antamoshkin's work it connects project requirements with implementation, integration, and operation in applied AI and digital-platform projects.", "AirScope and Siberiana provide applied contexts for architecture work, while engineering repositories demonstrate reproducible software and experimental infrastructure."),
        "ru": ("Архитектура программного обеспечения", "Архитектура программного обеспечения определяет структуру, интерфейсы и развитие сложных программных систем. В работе Олеслава Антамошкина она связывает требования проектов с реализацией, интеграцией и эксплуатацией прикладных AI-систем и цифровых платформ.", "AirScope и «Сибириана» дают прикладной контекст для архитектурной работы, а инженерные репозитории показывают воспроизводимую программную и экспериментальную инфраструктуру."),
    },
    "ai-systems": {
        "en": ("AI Systems", "AI systems combine data, models, software components, and operational workflows to solve a defined engineering problem. Oleslav Antamoshkin works on applied AI systems involving machine learning, decision support, computer vision, and platform integration.", "Relevant work includes computer-vision and UAV-data projects, multi-agent models, and AI-enabled software engineering repositories."),
        "ru": ("AI-системы", "AI-системы объединяют данные, модели, программные компоненты и рабочие процессы для решения определённой инженерной задачи. Олеслав Антамошкин работает с прикладными AI-системами, включающими машинное обучение, поддержку принятия решений, компьютерное зрение и интеграцию платформ.", "К этому направлению относятся проекты компьютерного зрения и БАС, многоагентные модели и репозитории, связанные с AI-поддержкой разработки."),
    },
    "agentic-software-engineering": {
        "en": ("Agentic Software Engineering", "Agentic software engineering applies autonomous and LLM-enabled agents to software and engineering workflows while preserving explicit evaluation, reproducibility, and human responsibility. Oleslav Antamoshkin's engineering work includes an LLM-agent policy loop in an adaptive distributed-computing research stand.", "The Adaptive Control of Heterogeneous Distributed Computing Systems repository links multi-agent models, ML forecasting, scheduling, load and failure scenarios, a CLI, web UI, and reproducibility protocols."),
        "ru": ("Агентная программная инженерия", "Агентная программная инженерия использует автономных и LLM-агентов в программных и инженерных процессах, сохраняя явную оценку, воспроизводимость и ответственность человека. В инженерной работе Олеслава Антамошкина контур политики LLM-агента входит в стенд адаптивного управления распределёнными вычислениями.", "Репозиторий Adaptive Control of Heterogeneous Distributed Computing Systems связывает многоагентные модели, ML-прогнозирование, планирование, сценарии нагрузки и отказов, CLI, веб-интерфейс и протоколы воспроизводимости."),
    },
    "distributed-systems": {
        "en": ("Distributed Systems", "Distributed systems coordinate computation and data across multiple nodes, services, or agents. Oleslav Antamoshkin's research profile includes heterogeneous information processing, multi-agent systems, decision support, adaptive scheduling, and distributed computing experiments.", "The adaptive-control repository and OptiNet simulation provide executable research infrastructure for this area."),
        "ru": ("Распределённые системы", "Распределённые системы координируют вычисления и данные между несколькими узлами, сервисами или агентами. Научный профиль Олеслава Антамошкина включает гетерогенную обработку информации, многоагентные системы, поддержку принятия решений, адаптивное планирование и эксперименты с распределёнными вычислениями.", "Репозиторий адаптивного управления и симуляция OptiNet дают исполняемую исследовательскую инфраструктуру этого направления."),
    },
    "computer-vision": {
        "en": ("Computer Vision", "Computer vision extracts usable information from images and video for detection, monitoring, and analytical tasks. Oleslav Antamoshkin's work includes UAV imagery, object detection, 3D reconstruction, and resource-aware model selection for edge deployment.", "AutoTinyCV and AirScope connect experimental computer vision with practical deployment constraints and spatial monitoring workflows."),
        "ru": ("Компьютерное зрение", "Компьютерное зрение извлекает полезную информацию из изображений и видео для обнаружения, мониторинга и аналитических задач. Работа Олеслава Антамошкина включает изображения БАС, обнаружение объектов, 3D-реконструкцию и ресурсно-ориентированный выбор моделей для периферийного развёртывания.", "AutoTinyCV и AirScope связывают экспериментальное компьютерное зрение с ограничениями практического внедрения и задачами пространственного мониторинга."),
    },
    "uav-spatial-monitoring": {
        "en": ("UAV Spatial Monitoring", "UAV spatial monitoring uses aerial data, photogrammetry, 3D reconstruction, point clouds, and computer vision to assess the condition and change of real-world objects. This is the central applied domain of AirScope, led scientifically and technically by Oleslav Antamoshkin.", "Relevant work includes AirScope, its AirBIM construction module, optimal flight-mission planning, and UAV-based tree-species detection."),
        "ru": ("Пространственный мониторинг по данным БАС", "Пространственный мониторинг по данным БАС использует аэрофотосъёмку, фотограмметрию, 3D-реконструкцию, облака точек и компьютерное зрение для оценки состояния и изменений реальных объектов. Это центральное прикладное направление AirScope, научно-техническим лидером которого является Олеслав Антамошкин.", "К направлению относятся AirScope, строительный модуль AirBIM, оптимальное планирование полётного задания и определение пород деревьев по данным БПЛА."),
    },
}


def nested_url(lang: str, section: str, slug: str) -> str:
    if section == "about":
        return site_url(f"{lang}/about")
    if section in {"expertise", "publications"} and slug == "index":
        return site_url(f"{lang}/{section}")
    return site_url(f"{lang}/{section}/{slug}")


def nested_breadcrumbs(lang: str, section: str, section_label: str, title: str, section_hub: bool = False) -> str:
    home = "Главная" if lang == "ru" else "Home"
    label = "Хлебные крошки" if lang == "ru" else "Breadcrumb"
    section_href = "./" if section_hub else ("../" if section in {"about", "expertise"} else f"../../{section}.html")
    home_href = "../index.html" if section == "about" or section_hub else "../../index.html"
    return (
        f'<nav class="breadcrumbs" aria-label="{label}"><ol>'
        f'<li><a href="{home_href}">{home}</a></li>'
        f'<li><a href="{section_href}">{html.escape(section_label)}</a></li>'
        f'<li aria-current="page">{html.escape(title)}</li>'
        "</ol></nav>"
    )


def render_nested_page(
    lang: str,
    section: str,
    slug: str,
    title: str,
    description: str,
    body: str,
    schema: dict[str, object],
    section_label: str,
    other_slug: str | None = None,
    section_hub: bool = False,
) -> str:
    meta = LANG_META[lang]
    other = meta["other"]
    other_slug = other_slug or slug
    url = nested_url(lang, section, slug)
    other_url = nested_url(other, section, other_slug)
    page_title = f"{title} | {meta['site']}"
    nav_label = "Основная навигация" if lang == "ru" else "Primary navigation"
    relative_root = "../" if section == "about" or section_hub else "../../"
    graph = [person_entity(), {"@type": "WebSite", "@id": site_url("#website"), "url": site_url(), "name": "Oleslav Antamoshkin"}, schema]
    graph.append({
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": site_url()},
            {"@type": "ListItem", "position": 2, "name": section_label, "item": nested_url(lang, section, slug) if section == "about" else site_url(page_path(lang, section))},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    })
    json_ld = json_script({"@context": "https://schema.org", "@graph": graph})
    nav = "\n".join(
        f'<a href="{relative_root}{page_href(item_slug)}">{html.escape(labels[lang])}</a>'
        for item_slug, labels in PAGES
    )
    return f"""<!doctype html>
<html lang="{meta['html_lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{html.escape(url, quote=True)}">
  <link rel="alternate" hreflang="en" href="{html.escape(nested_url('en', section, slug), quote=True)}">
  <link rel="alternate" hreflang="ru" href="{html.escape(nested_url('ru', section, slug), quote=True)}">
  <link rel="alternate" hreflang="x-default" href="{html.escape(nested_url('en', section, slug), quote=True)}">
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{'ru_RU' if lang == 'ru' else 'en_US'}">
  <meta property="og:title" content="{html.escape(page_title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{html.escape(url, quote=True)}">
  <meta property="og:image" content="{html.escape(site_url(OG_IMAGE), quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(page_title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{html.escape(site_url(OG_IMAGE), quote=True)}">
  <link rel="stylesheet" href="../../styles.css?v={ASSET_VERSION}">
  {json_ld}
</head>
<body>
  <a class="skip-link" href="#content">{html.escape(meta['skip'])}</a>
  <header class="site-header">
    <div class="brand"><a href="{relative_root}index.html" aria-label="{html.escape(meta['site'])}">OA</a><span>{html.escape(meta['role'])}</span></div>
    <nav class="site-nav" aria-label="{nav_label}">{nav}</nav>
    <a class="language-link" href="{'../../' + other + '/about/' if section == 'about' else '../../' + other + '/' + section + '/' if section_hub else '../../../' + other + '/' + section + '/' + other_slug + '/'}">{LANG_META[other]['name']}</a>
  </header>
  <main id="content" class="content page-{section}-entity">
    {nested_breadcrumbs(lang, section, section_label, title, section_hub)}
    {body}
  </main>
  <footer class="site-footer"><span>{html.escape(meta['footer'])}</span></footer>
</body>
</html>
"""


def render_project_entity(lang: str, slug: str) -> str:
    data = PROJECT_ENTITIES[slug][lang]
    labels = {
        "en": ("Projects", "Overview", "Problem", "Approach and architecture", "Applications", "Results", "External reference", "Related expertise"),
        "ru": ("Проекты", "Обзор", "Задача", "Подход и архитектура", "Применение", "Результаты", "Внешняя ссылка", "Связанная экспертиза"),
    }[lang]
    expertise = "../../expertise/uav-spatial-monitoring/" if slug == "airscope" else "../../expertise/software-architecture/"
    expertise_label = "UAV spatial monitoring" if slug == "airscope" else "Software architecture"
    if lang == "ru":
        expertise_label = "Пространственный мониторинг по данным БАС" if slug == "airscope" else "Архитектура программного обеспечения"
    external_name, external_url = data["external"]
    body = (
        f"<article class=\"entity-page\"><h1>{html.escape(data['title'])}</h1><p class=\"answer-first\">{html.escape(data['answer'])}</p>"
        f"<h2>{labels[1]}</h2><p>{html.escape(data['description'])}</p>"
        f"<h2>{labels[2]}</h2><p>{html.escape(data['problem'])}</p>"
        f"<h2>{labels[3]}</h2><p>{html.escape(data['approach'])}</p>"
        f"<h2>{labels[4]}</h2><p>{html.escape(data['applications'])}</p>"
        f"<h2>{labels[5]}</h2><p>{html.escape(data['results'])}</p>"
        f"<h2>{labels[6]}</h2><p><a href=\"{html.escape(external_url, quote=True)}\" rel=\"noreferrer\">{html.escape(external_name)}</a></p>"
        f"<h2>{labels[7]}</h2><p><a href=\"{expertise}\">{html.escape(expertise_label)}</a></p></article>"
    )
    schema = {
        "@type": "SoftwareApplication", "@id": f"{nested_url(lang, 'projects', slug)}#software",
        "url": nested_url(lang, "projects", slug), "name": "AirScope" if slug == "airscope" else "Siberiana",
        "description": data["description"], "author": {"@id": PERSON_ID}, "dateModified": BUILD_DATE,
    }
    return render_nested_page(lang, "projects", slug, data["title"], data["description"], body, schema, labels[0])


def render_expertise_entity(lang: str, slug: str) -> str:
    title, answer, evidence = EXPERTISE_ENTITIES[slug][lang]
    section_label = "Экспертиза" if lang == "ru" else "Expertise"
    related = "../../projects/airscope/" if slug in {"computer-vision", "uav-spatial-monitoring"} else "../../projects.html"
    project_label = "AirScope" if slug in {"computer-vision", "uav-spatial-monitoring"} else ("Проекты" if lang == "ru" else "Projects")
    body = (
        f"<article class=\"entity-page\"><h1>{html.escape(title)}</h1><p class=\"answer-first\">{html.escape(answer)}</p>"
        f"<h2>{'Связь с работой' if lang == 'ru' else 'Relation to the work'}</h2><p>{html.escape(evidence)}</p>"
        f"<h2>{'Связанные проекты и репозитории' if lang == 'ru' else 'Related projects and repositories'}</h2><p><a href=\"{related}\">{project_label}</a> · <a href=\"../../publications.html\">{'Публикации' if lang == 'ru' else 'Publications'}</a> · <a href=\"https://github.com/oleslav24\">GitHub</a></p></article>"
    )
    description = answer
    schema = {"@type": "DefinedTerm", "@id": f"{nested_url(lang, 'expertise', slug)}#topic", "name": title, "description": description, "inDefinedTermSet": site_url("#expertise"), "url": nested_url(lang, "expertise", slug)}
    return render_nested_page(lang, "expertise", slug, title, description, body, schema, section_label)


def render_expertise_hub(lang: str) -> str:
    title = "Экспертиза" if lang == "ru" else "Expertise"
    description = "Ключевые инженерные и исследовательские направления Олеслава Антамошкина." if lang == "ru" else "Key engineering and research areas of Oleslav Antamoshkin."
    links = []
    for slug, localized in EXPERTISE_ENTITIES.items():
        item_title, answer, _evidence = localized[lang]
        links.append(f'<li><a href="{slug}/">{html.escape(item_title)}</a><br>{html.escape(answer)}</li>')
    body = f'<article class="entity-page"><h1>{title}</h1><p class="answer-first">{html.escape(description)}</p><ul>{"".join(links)}</ul></article>'
    schema = {"@type": "CollectionPage", "@id": f"{nested_url(lang, 'expertise', 'index')}#collection", "url": nested_url(lang, "expertise", "index"), "name": title, "description": description, "author": {"@id": PERSON_ID}}
    return render_nested_page(lang, "expertise", "index", title, description, body, schema, title, section_hub=True)


def render_publications_hub(lang: str) -> str:
    body = render_publications_page(lang)
    body = body.replace('href="../downloads/', 'href="../../downloads/')
    body = body.replace('href="publications/', 'href="')
    title = "Публикации" if lang == "ru" else "Publications"
    description = page_description(lang, "publications")
    schema = {
        "@type": "CollectionPage", "@id": f"{nested_url(lang, 'publications', 'index')}#collection",
        "url": nested_url(lang, "publications", "index"), "name": title,
        "description": description, "author": {"@id": PERSON_ID}, "dateModified": BUILD_DATE,
    }
    return render_nested_page(lang, "publications", "index", title, description, body, schema, title, section_hub=True)


def render_about_entity(lang: str) -> str:
    markdown = (CONTENT_DIR / lang / "about.md").read_text(encoding="utf-8")
    title = first_heading(markdown, "Oleslav Antamoshkin")
    description = page_description(lang, "about")
    schema = {
        "@type": "ProfilePage", "@id": f"{nested_url(lang, 'about', 'profile')}#profile",
        "url": nested_url(lang, "about", "profile"), "headline": title,
        "description": description, "mainEntity": {"@id": PERSON_ID},
        "dateModified": BUILD_DATE,
    }
    # The route is /{lang}/about; the generic nested helper uses a leaf directory.
    body = markdown_to_html(markdown)
    return render_nested_page(lang, "about", "profile", title, description, body, schema, "Профиль" if lang == "ru" else "Profile")


def publication_slug(publication: dict[str, str], lang: str) -> str:
    title = localized_publication_parts(publication, lang)["title"].lower()
    ascii_title = re.sub(r"[^a-z0-9]+", "-", title).strip("-")
    return f"{publication['number']}-{ascii_title[:72] or 'publication'}"


def extract_doi(value: str) -> str | None:
    match = re.search(r"\b10\.\d{4,9}/[-._;()/:a-z0-9]+", value, re.IGNORECASE)
    return match.group(0).rstrip(".,;") if match else None


def publication_is_indexable(publication: dict[str, str], selected_numbers: set[str], recent_numbers: set[str]) -> bool:
    return publication["number"] in selected_numbers or publication["number"] in recent_numbers or bool(extract_doi(publication["gost"]))


def publication_page_href(publication: dict[str, str], lang: str) -> str | None:
    if publication["number"] in SELECTED_PUBLICATION_NUMBERS or int(publication["number"]) >= 182 or extract_doi(publication["gost"]):
        return f"publications/{publication_slug(publication, lang)}/"
    return None


def render_publication_entity(lang: str, publication: dict[str, str]) -> str:
    data = localized_publication_parts(publication, lang)
    slug = publication_slug(publication, lang)
    doi = extract_doi(data["details"]) or extract_doi(publication["gost"])
    labels = {
        "en": ("Publications", "Authors", "Year", "Publication venue", "DOI", "Citation", "All publications"),
        "ru": ("Публикации", "Авторы", "Год", "Издание", "DOI", "Цитирование", "Все публикации"),
    }[lang]
    citation = localize_publication_text(publication, publication["citations"]["gost"], lang)
    doi_html = f'<a href="https://doi.org/{html.escape(doi, quote=True)}">{html.escape(doi)}</a>' if doi else ""
    body = [f'<article class="entity-page publication-entity"><h1>{html.escape(data["title"])}</h1>']
    body.append(f"<h2>{labels[1]}</h2><p>{html.escape(data['authors'])}</p>")
    body.append(f"<h2>{labels[2]}</h2><p>{html.escape(publication['year'])}</p>")
    if data["details"]:
        body.append(f"<h2>{labels[3]}</h2><p>{html.escape(data['details'])}</p>")
    if doi_html:
        body.append(f"<h2>{labels[4]}</h2><p>{doi_html}</p>")
    body.append(f"<h2>{labels[5]}</h2><p class=\"citation\">{html.escape(citation)}</p>")
    body.append(f'<p><a href="../../publications.html">{labels[6]}</a></p></article>')
    authors: list[dict[str, str]] = []
    for author in re.split(r",\s*", data["authors"]):
        if "Antamoshkin" in author or "Антамошкин" in author:
            authors.append({"@id": PERSON_ID})
        elif author:
            authors.append({"@type": "Person", "name": author})
    schema: dict[str, object] = {
        "@type": "ScholarlyArticle", "@id": f"{nested_url(lang, 'publications', slug)}#article",
        "url": nested_url(lang, "publications", slug), "headline": data["title"],
        "datePublished": publication["year"], "author": authors,
    }
    if doi:
        schema["identifier"] = [{"@type": "PropertyValue", "propertyID": "DOI", "value": doi}]
        schema["sameAs"] = f"https://doi.org/{doi}"
    return render_nested_page(lang, "publications", slug, data["title"], data["details"] or data["title"], "\n".join(body), schema, labels[0], publication_slug(publication, "ru" if lang == "en" else "en"))


def root_json_ld() -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            person_entity(),
            {
                "@type": "WebSite",
                "@id": site_url("#website"),
                "url": site_url(),
                "name": "Oleslav Antamoshkin",
                "inLanguage": ["en", "ru"],
            },
            {
                "@type": "ProfilePage",
                "@id": site_url("#profile"),
                "headline": "Oleslav Antamoshkin",
                "description": "Software and AI architect profile of Oleslav Antamoshkin.",
                "author": {"@id": PERSON_ID},
                "mainEntityOfPage": site_url(),
                "inLanguage": "en",
                "dateModified": BUILD_DATE,
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


def render_root_legacy() -> str:
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
  <link rel="stylesheet" href="{stylesheet}">
  {json_ld}
</head>
<body>
  <a class="skip-link" href="#content">К содержанию</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="Олеслав Антамошкин" aria-current="page">ОА</a>
      <span>Архитектура ПО · AI-системы · прикладная разработка</span>
    </div>
    <nav class="site-nav" aria-label="Основная навигация">
      <a class="active" href="index.html" aria-current="page">Главная</a>
      <a href="ru/projects.html">Проекты</a>
      <a href="ru/experience.html">Опыт</a>
      <a href="ru/research.html">Исследования</a>
      <a href="ru/publications.html">Публикации</a>
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
    <p>Архитектор программных и AI-систем</p>
    <p>Распределённые системы · AI-платформы · Техническое руководство</p>
    <p>Проектирую и веду разработку сложных программных и AI-систем: от архитектуры и технического задания до реализации, интеграции и внедрения.</p>
    <p>Доктор технических наук, заведующий кафедрой программной инженерии Сибирского федерального университета.</p>
    <section class="profile-anchor" aria-label="Текущие роли">
      <div class="profile-anchor-text">
        <p class="section-kicker">Текущие роли</p>
        <ul class="compact-role-list">
          <li>Заведующий кафедрой программной инженерии ИКИТ СФУ.</li>
          <li>Профессор кафедры информационных технологий в креативных и культурных индустриях ГИ СФУ.</li>
          <li>Научно-технический лидер AirScope и руководитель платформы «Сибириана».</li>
        </ul>
      </div>
      <img class="profile-photo" src="assets/profile-portrait-bw-site.webp" alt="Олеслав Антамошкин" width="960" height="960" loading="eager" decoding="async">
    </section>
    <div class="gate-links" aria-label="Основные разделы">
      <a href="ru/projects.html">Проекты</a>
      <a href="ru/publications.html">Публикации</a>
      <a href="ru/contacts.html">Контакты</a>
    </div>
  </main>
  <footer class="site-footer">
    <span>© 2026 Олеслав Антамошкин · Архитектура ПО · AI-системы · Прикладная разработка</span>
  </footer>
</body>
</html>
""".format(
        description=html.escape(description),
        url=html.escape(site_url(), quote=True),
        image=html.escape(site_url(OG_IMAGE), quote=True),
        alternate=alternate_links(),
        json_ld=root_json_ld(),
        stylesheet=html.escape(versioned_asset("styles.css"), quote=True),
    )


def render_root() -> str:
    title = HOMEPAGE_TITLES["en"]
    description = PAGE_DESCRIPTIONS["en"]["index"]
    url = html.escape(site_url(), quote=True)
    image = html.escape(site_url(OG_IMAGE), quote=True)
    stylesheet = html.escape(versioned_asset("styles.css"), quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{url}">
{alternate_links()}
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(description)}">
  <meta name="twitter:image" content="{image}">
  <link rel="stylesheet" href="{stylesheet}">
  {root_json_ld()}
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="brand">
      <a href="index.html" aria-label="Oleslav Antamoshkin" aria-current="page">OA</a>
      <span>Software Architecture · AI Systems · Applied Engineering</span>
    </div>
    <nav class="site-nav" aria-label="Primary navigation">
      <a class="active" href="index.html" aria-current="page">Home</a>
      <a href="en/projects.html">Projects</a>
      <a href="en/experience.html">Experience</a>
      <a href="en/research.html">Research</a>
      <a href="en/publications.html">Publications</a>
      <a href="en/contacts.html">Contact</a>
      <a href="ru/index.html">RU</a>
    </nav>
  </header>
  <main id="content" class="content page-root">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <ol>
        <li aria-current="page">Profile</li>
      </ol>
    </nav>
    <h1>Oleslav Antamoshkin</h1>
    <p>Software &amp; AI Architect</p>
    <p>Distributed Systems · AI Platforms · Engineering Leadership</p>
    <p class="hero-summary">I design and lead the development of complex software and AI systems, from architecture and technical specifications to implementation, integration, and deployment.</p>
    <p class="hero-roles">Doctor of Engineering Sciences. Head of the Software Engineering Department at Siberian Federal University.</p>
    <p class="name-variant">Russian spelling: Олеслав Антамошкин.</p>
    <section class="profile-anchor" aria-label="Current roles">
      <div class="profile-anchor-text">
        <p class="section-kicker">Current roles</p>
        <ul class="compact-role-list">
          <li>Head of the Software Engineering Department, Siberian Federal University.</li>
          <li>Professor at the Department of Information Technologies in Creative and Cultural Industries, Siberian Federal University.</li>
          <li>Scientific and technical lead for AirScope; project lead for Siberiana.</li>
        </ul>
      </div>
      <img class="profile-photo" src="assets/profile-portrait-bw-site.webp" alt="Oleslav Antamoshkin" width="960" height="960" loading="eager" decoding="async">
    </section>
    <section aria-labelledby="engineering-focus">
      <p class="section-kicker">Engineering focus</p>
      <h2 id="engineering-focus">Complex systems, built for use</h2>
      <div class="direction-grid">
        <article><h3>Software Architecture</h3><p>Architecture for complex, evolving software products and services.</p></article>
        <article><h3>Distributed Systems</h3><p>Multi-service and distributed computing systems with reliable integration boundaries.</p></article>
        <article><h3>Artificial Intelligence</h3><p>Machine learning, multi-agent systems, and LLM-enabled engineering workflows.</p></article>
        <article><h3>Computer Vision</h3><p>Vision systems for imagery, monitoring, detection, and analytical tasks.</p></article>
        <article><h3>UAV and Spatial Data</h3><p>UAV data pipelines, photogrammetry, 3D reconstruction, and spatial analytics.</p></article>
        <article><h3>Digital Platforms</h3><p>Applied platforms that connect data, engineering processes, and decision-making.</p></article>
      </div>
    </section>
    <section aria-labelledby="featured-projects">
      <p class="section-kicker">Featured projects</p>
      <h2 id="featured-projects">Software &amp; AI systems</h2>
      <div class="project-showcase">
        <article><h3>AirScope</h3><p>UAV-based spatial monitoring platform for construction, infrastructure, and industrial objects.</p><p><strong>Role:</strong> Scientific and technical lead.</p><p><strong>Focus:</strong> UAV data, photogrammetry, 3D models, point clouds, and computer vision.</p><p><a href="en/projects.html">View project</a></p></article>
        <article><h3>Siberiana</h3><p>Digital platform for cultural, historical, and regional information resources of Yenisei Siberia.</p><p><strong>Role:</strong> Project lead.</p><p><strong>Focus:</strong> Platform architecture, data integration, search, and digital archives.</p><p><a href="en/projects.html">View project</a></p></article>
        <article><h3>Adaptive Control of Heterogeneous Distributed Computing Systems</h3><p>Research engineering repository for adaptive scheduling and control in distributed computing environments.</p><p><strong>Focus:</strong> Distributed systems, optimization, and computational experiments.</p><p><a href="https://github.com/oleslav24/Adaptive-control-of-heterogeneous-distributed-computing-systems">View on GitHub</a></p></article>
      </div>
    </section>
    <section aria-labelledby="what-i-do">
      <p class="section-kicker">What I do</p>
      <h2 id="what-i-do">From system design to delivery</h2>
      <ul>
        <li>Design software and AI system architectures.</li>
        <li>Lead engineering teams and applied R&amp;D projects.</li>
        <li>Develop AI, computer vision, and UAV-data solutions.</li>
        <li>Build digital platforms and decision-support systems.</li>
      </ul>
    </section>
    <div class="gate-links" aria-label="Primary sections">
      <a href="en/projects.html">View Projects</a>
      <a href="https://github.com/oleslav24">GitHub</a>
      <a href="en/contacts.html">Contact</a>
    </div>
  </main>
  <footer class="site-footer">
    <span>© 2026 Oleslav Antamoshkin · Software Architecture · AI Systems · Applied Engineering</span>
  </footer>
</body>
</html>
"""


def render_sitemap() -> str:
    urls = [("", "1.0")]
    for lang in ("en", "ru"):
        for slug, _labels in PAGES:
            urls.append((page_path(lang, slug), "0.8" if slug != "index" else "0.9"))
        urls.append((f"{lang}/about", "0.9"))
        urls.append((f"{lang}/expertise", "0.8"))
        for project_slug in PROJECT_ENTITIES:
            urls.append((f"{lang}/projects/{project_slug}", "0.8"))
        for expertise_slug in EXPERTISE_ENTITIES:
            urls.append((f"{lang}/expertise/{expertise_slug}", "0.7"))
    publications = load_publications()
    recent_numbers = {item["number"] for item in sorted(publications, key=publication_sort_key, reverse=True)[:10]}
    selected_numbers = set(SELECTED_PUBLICATION_NUMBERS)
    for lang in ("en", "ru"):
        for publication in publications:
            if publication_is_indexable(publication, selected_numbers, recent_numbers):
                urls.append((f"{lang}/publications/{publication_slug(publication, lang)}", "0.6"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(site_url(path))}</loc>")
        lines.append(f"    <lastmod>{BUILD_DATE}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)


def render_robots() -> str:
    agents = [
        "*", "OAI-SearchBot", "GPTBot", "ClaudeBot", "Claude-SearchBot",
        "Claude-User", "PerplexityBot", "Google-Extended",
    ]
    rules = []
    for agent in agents:
        rules.extend([f"User-agent: {agent}", "Allow: /", ""])
    return "\n".join(rules) + f"Sitemap: {site_url('sitemap.xml')}\n"


def render_llms() -> str:
    return """# Oleslav Antamoshkin

> Official professional and research website of Oleslav Antamoshkin, Software & AI Architect, Doctor of Engineering Sciences and Head of the Software Engineering Department at Siberian Federal University.

## Profile
- https://oleslav.com/en/about

## Expertise
- https://oleslav.com/en/expertise/software-architecture
- https://oleslav.com/en/expertise/ai-systems
- https://oleslav.com/en/expertise/agentic-software-engineering
- https://oleslav.com/en/expertise/distributed-systems
- https://oleslav.com/en/expertise/computer-vision
- https://oleslav.com/en/expertise/uav-spatial-monitoring

## Projects
- https://oleslav.com/en/projects/airscope
- https://oleslav.com/en/projects/siberiana

## Publications
- https://oleslav.com/en/publications.html

## Russian version
- https://oleslav.com/ru/index.html

## External identifiers
- ORCID: https://orcid.org/0000-0002-5976-5847
- Web of Science ResearcherID: https://www.webofscience.com/wos/author/rid/Q-7307-2018
- Scopus Author ID: https://www.scopus.com/authid/detail.uri?authorId=56825984000
- RSCI Author ID: https://elibrary.ru/author_profile.asp?id=501153
"""


def render_redirects() -> str:
    return """https://www.oleslav.com/* https://oleslav.com/:splat 301
http://oleslav.com/* https://oleslav.com/:splat 301
http://www.oleslav.com/* https://oleslav.com/:splat 301
"""


def render_headers() -> str:
    return """/downloads/publications-*.pdf
  X-Robots-Tag: noindex
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
  <desc id="desc">Software and AI architecture, distributed systems, and applied engineering</desc>
  <rect width="1200" height="630" fill="#ffffff"/>
  <rect x="72" y="72" width="220" height="220" fill="#111111"/>
  <text x="182" y="218" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="92" font-weight="700" text-anchor="middle">OA</text>
  <text x="72" y="390" fill="#111111" font-family="Arial, Helvetica, sans-serif" font-size="64" font-weight="700">Oleslav Antamoshkin</text>
  <text x="72" y="455" fill="#606060" font-family="Arial, Helvetica, sans-serif" font-size="32">Software &amp; AI Architect</text>
  <line x1="72" y1="508" x2="1128" y2="508" stroke="#d8d8d8" stroke-width="2"/>
  <text x="72" y="560" fill="#606060" font-family="Arial, Helvetica, sans-serif" font-size="24">Distributed systems · AI platforms · Engineering leadership</text>
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
  <link rel="stylesheet" href="{stylesheet}">
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
    <span>© 2026 Oleslav Antamoshkin · Software Architecture · AI Systems · Applied Engineering</span>
  </footer>
</body>
</html>
""".format(
        description=html.escape(description),
        url=html.escape(site_url("404.html"), quote=True),
        alternate=alternate_links(),
        stylesheet=html.escape(versioned_asset("styles.css"), quote=True),
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

        about_destination = PUBLIC_DIR / lang / "about" / "index.html"
        about_destination.parent.mkdir(parents=True, exist_ok=True)
        about_destination.write_text(render_about_entity(lang), encoding="utf-8")

        for project_slug in PROJECT_ENTITIES:
            destination = PUBLIC_DIR / lang / "projects" / project_slug / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(render_project_entity(lang, project_slug), encoding="utf-8")

        for expertise_slug in EXPERTISE_ENTITIES:
            destination = PUBLIC_DIR / lang / "expertise" / expertise_slug / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(render_expertise_entity(lang, expertise_slug), encoding="utf-8")

        expertise_destination = PUBLIC_DIR / lang / "expertise" / "index.html"
        expertise_destination.parent.mkdir(parents=True, exist_ok=True)
        expertise_destination.write_text(render_expertise_hub(lang), encoding="utf-8")

        publications = load_publications()
        recent_numbers = {item["number"] for item in sorted(publications, key=publication_sort_key, reverse=True)[:10]}
        selected_numbers = set(SELECTED_PUBLICATION_NUMBERS)
        for publication in publications:
            if not publication_is_indexable(publication, selected_numbers, recent_numbers):
                continue
            destination = PUBLIC_DIR / lang / "publications" / publication_slug(publication, lang) / "index.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(render_publication_entity(lang, publication), encoding="utf-8")

        publications_destination = PUBLIC_DIR / lang / "publications" / "index.html"
        publications_destination.parent.mkdir(parents=True, exist_ok=True)
        publications_destination.write_text(render_publications_hub(lang), encoding="utf-8")

    (PUBLIC_DIR / "index.html").write_text(render_root(), encoding="utf-8")
    (PUBLIC_DIR / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")
    (PUBLIC_DIR / "robots.txt").write_text(render_robots(), encoding="utf-8")
    (PUBLIC_DIR / "llms.txt").write_text(render_llms(), encoding="utf-8")
    (PUBLIC_DIR / "_redirects").write_text(render_redirects(), encoding="utf-8")
    (PUBLIC_DIR / "_headers").write_text(render_headers(), encoding="utf-8")
    (PUBLIC_DIR / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (PUBLIC_DIR / "favicon.svg").write_text(render_favicon(), encoding="utf-8")
    (PUBLIC_DIR / OG_IMAGE).write_text(render_og_image(), encoding="utf-8")
    (PUBLIC_DIR / "404.html").write_text(render_404(), encoding="utf-8")
    build_publication_pdf_exports()


if __name__ == "__main__":
    build()
