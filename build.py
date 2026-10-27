"""Builds index.html (English) and es/index.html (Spanish) from src/page.html.

Edit src/page.html, then run:  python3 build.py

English text sits inside each element. Its Spanish version sits on the same
element's data-es attribute. Needs: pip install beautifulsoup4
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup

SITE = "https://cynthiaricocook.com/"
ROOT = Path(__file__).parent

PAGES = {
    "en": {
        "out": "index.html",
        "base": "",
        "url": SITE,
        "locale": "en_US",
        "title": "Cynthia Rico Cook | Websites and web tools for your business",
        "desc": "I build websites and web tools for your business: sites that get you found, tools built around how you work, and fixes for what you already have. English y español. Twin Cities, Minnesota.",
        "ogalt": "Black-eyed Susans by a lake, with the words Websites for small businesses",
        "alt1": "A chaga mushroom shaped like a heart, growing on a birch tree",
        "alt2": "A harvest of dandelions",
        "alt3": "Foraged wild plants",
        "alt4": "The quote calculator showing a price estimate",
        "alt5": "Rows of strawberry beds under a low sunset",
        "alt6": "Cynthia smiling outdoors with a yellow flower in her hair",
        "alt7": "Black-eyed Susans blooming beside a lake in the Twin Cities",
        "alt8": "A lake at sunset with the sky turning orange",
        "alt9": "Wildflowers in front of a snowy Mount Rainier",
        "services": ["Websites", "Custom web tools for small businesses", "Website fixes and upkeep"],
    },
    "es": {
        "out": "es/index.html",
        "base": "../",
        "url": SITE + "es/",
        "locale": "es_US",
        "title": "Cynthia Rico Cook | Sitios web y herramientas para tu negocio",
        "desc": "Hago sitios web y herramientas para tu negocio: sitios para que te encuentren, herramientas hechas a la medida de tu negocio y arreglos para lo que ya tienes. Español e inglés. Twin Cities, Minnesota.",
        "ogalt": "Rudbeckias junto a un lago, con las palabras Sitios web para negocios pequeños",
        "alt1": "Un hongo chaga con forma de corazón en un abedul",
        "alt2": "Una cosecha de dientes de león",
        "alt3": "Plantas silvestres recolectadas",
        "alt4": "La calculadora mostrando un precio estimado",
        "alt5": "Hileras de fresas bajo el sol de la tarde",
        "alt6": "Cynthia sonriendo al aire libre con una flor amarilla en el pelo",
        "alt7": "Flores de rudbeckia junto a un lago en las Twin Cities",
        "alt8": "Un lago al atardecer con el cielo anaranjado",
        "alt9": "Flores silvestres frente al Monte Rainier nevado",
        "services": ["Sitios web", "Herramientas web a la medida para negocios pequeños", "Arreglos y mantenimiento de sitios web"],
    },
}


def json_ld(lang, page):
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": "Cynthia Rico Cook",
            "description": page["desc"],
            "url": page["url"],
            "image": SITE + "img/og.jpg",
            "inLanguage": lang,
            "knowsLanguage": ["en", "es"],
            "areaServed": {"@type": "Place", "name": "Minneapolis-Saint Paul, Minnesota"},
            "address": {"@type": "PostalAddress", "addressRegion": "MN", "addressCountry": "US"},
            "founder": {"@type": "Person", "name": "Cynthia Rico Cook"},
            "makesOffer": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name}}
                for name in page["services"]
            ],
        },
        ensure_ascii=False,
    )


def lang_links(lang):
    en = '<a href="{}" {}>EN</a>'.format("./" if lang == "en" else "../", 'aria-current="page"' if lang == "en" else 'hreflang="en"')
    es = '<a href="{}" {}>ES</a>'.format("es/" if lang == "en" else "./", 'aria-current="page"' if lang == "es" else 'hreflang="es"')
    return en + "<span>/</span>" + es


def build(lang, page):
    html = (ROOT / "src/page.html").read_text(encoding="utf-8")
    fills = {
        "LANG": lang, "TITLE": page["title"], "DESC": page["desc"], "URL": page["url"],
        "SITE": SITE, "BASE": page["base"], "LOCALE": page["locale"], "OGALT": page["ogalt"],
        "ALT1": page["alt1"], "ALT2": page["alt2"], "ALT3": page["alt3"], "ALT4": page["alt4"], "ALT5": page["alt5"], "ALT6": page["alt6"], "ALT7": page["alt7"], "ALT8": page["alt8"], "ALT9": page["alt9"],
        "JSONLD": json_ld(lang, page), "LANGLINKS": lang_links(lang),
    }
    for key, value in fills.items():
        html = html.replace("{{" + key + "}}", value)

    soup = BeautifulSoup(html, "html.parser")
    for el in soup.select("[data-es]"):
        if lang == "es":
            el.clear()
            el.append(BeautifulSoup(el["data-es"], "html.parser"))
        del el["data-es"]

    out = ROOT / page["out"]
    out.parent.mkdir(exist_ok=True)
    out.write_text(str(soup), encoding="utf-8")
    print("wrote", page["out"])


for lang, page in PAGES.items():
    build(lang, page)
