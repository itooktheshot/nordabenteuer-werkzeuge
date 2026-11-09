#!/usr/bin/env python3
"""Baut werkzeuge.nordabenteuer.de (Deutsch und Englisch) nach docs/.

    src/*.html      deutsche Werkzeuge   → docs/<slug>/index.html
    src/en/*.html   englische Werkzeuge  → docs/en/<slug>/index.html
    assets/         nab.css, zahlen.js (ALLE veränderlichen Zahlen), Schriften, Favicon

Jede Datei in src/ ist ein eigenständiges Werkzeug (Stil, Markup, Skript) ohne
<html>/<head>. Dieses Skript legt Kopfleiste, Fußleiste, Meta-Daten, hreflang
und die gemeinsame Gestaltung darum.

    python3 build.py

Danach committen und pushen — GitHub Pages liefert docs/ aus.
"""
import re, json, shutil, hashlib, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC, OUT, ASSETS = ROOT / "src", ROOT / "docs", ROOT / "assets"
HOST = "https://werkzeuge.nordabenteuer.de"
MAIN = "https://www.nordabenteuer.de"
TODAY = datetime.date.today().isoformat()


def ver(name):  # Cache-Busting: Versionsparameter aus dem Dateiinhalt
    return hashlib.md5((ASSETS / name).read_bytes()).hexdigest()[:8]


CSSV, ZAHLENV = ver("nab.css"), ver("zahlen.js")
KOMMUNV = ver("kommunpreise.js")  # nur die Hauspreis-Seite laedt diese Datei

# Jedes Werkzeug in beiden Sprachen. Die Paare bestimmen hreflang und den Sprachumschalter.
TOOLS = [
    dict(color="a",
         de=dict(slug="inserat-auf-deutsch", src="inserat-auf-deutsch.html", kick="Immobilien",
                 title="Inserat auf Deutsch",
                 card="Faktenliste eines schwedischen Inserats einfügen — jede Zeile erklärt, dazu Preis je m², Avgift im Jahr und die Stämpelskatt, die im Inserat fehlt.",
                 desc="Schwedisches Immobilieninserat verstehen: Utgångspris, Avgift, Boarea, Driftkostnad auf Deutsch erklärt und die fehlenden Zahlen ausgerechnet. Läuft im Browser, nichts wird hochgeladen."),
         en=dict(slug="read-a-swedish-listing", src="en/read-a-swedish-listing.html", kick="Property",
                 title="Read a Swedish listing",
                 card="Paste the fact list from a Swedish property listing — every line explained, plus price per m², the yearly fee and the stamp duty the listing leaves out.",
                 desc="Understand a Swedish property listing: Utgångspris, Avgift, Boarea, Driftkostnad explained in English, with the missing numbers calculated. Works with Hemnet in Swedish or English. Runs in your browser.")),
    dict(color="b",
         de=dict(slug="kaufnebenkosten", src="kaufnebenkosten-schweden.html", kick="Immobilien",
                 title="Kaufnebenkosten Schweden",
                 card="Stämpelskatt, Pantbrev, Gebühren und die jährliche Fastighetsavgift — was beim Hauskauf in Schweden zum Kaufpreis dazukommt.",
                 desc="Kaufnebenkosten beim Hauskauf in Schweden berechnen: Stämpelskatt 1,5 %, Pantbrev 2 %, Lagfart-Gebühr, Fastighetsavgift. Mit Bostadsrätt, Äganderätt und Tomträtt."),
         en=dict(slug="buying-costs-sweden", src="en/buying-costs-sweden.html", kick="Property",
                 title="Buying costs in Sweden",
                 card="Stamp duty, mortgage deeds, fees and the yearly property charge — what comes on top of the price when you buy a home in Sweden.",
                 desc="Calculate the costs of buying a home in Sweden: stamp duty 1.5 %, mortgage deeds 2 %, title registration fee, property charge. For bostadsrätt, freehold and tomträtt.")),
    dict(color="c",
         de=dict(slug="fragen-an-den-maeklare", src="fragen-an-den-maeklare.html", kick="Besichtigung",
                 title="Fragen an den Mäklare",
                 card="48 Fragen für die Visning, nach Objektart sortiert — jede auf Schwedisch und Deutsch, zum Kopieren.",
                 desc="Fragen an den Mäklare bei der Besichtigung in Schweden: Bostadsrätt, Haus oder Ferienhaus. Schwedischer Wortlaut mit deutscher Übersetzung, als Liste zum Mitnehmen."),
         en=dict(slug="questions-for-the-estate-agent", src="en/questions-for-the-estate-agent.html", kick="Viewing",
                 title="Questions for the estate agent",
                 card="48 questions for the viewing, sorted by property type — each in Swedish and English, ready to copy.",
                 desc="What to ask the Swedish estate agent (mäklare) at a viewing: apartment, house or holiday home. Swedish wording with English translation, as a list to take along.")),
    dict(color="d",
         de=dict(slug="behoerden-reihenfolge", src="behoerden-reihenfolge.html", kick="Umzug",
                 title="Behörden-Reihenfolge Schweden",
                 card="Personnummer, ID-kort, Bankkonto, BankID — in welcher Reihenfolge, und was wovon abhängt. Nach Dauer, Status und Kindern.",
                 desc="Behördengänge nach dem Umzug nach Schweden in der richtigen Reihenfolge: Skatteverket, Personnummer, ID-kort, Bankkonto, BankID, Försäkringskassan — angepasst an deine Lage."),
         en=dict(slug="authorities-order-sweden", src="en/authorities-order-sweden.html", kick="Moving",
                 title="Swedish authorities: what comes first",
                 card="Residence permit, personnummer, ID card, bank, BankID — in which order, and what depends on what. By citizenship, length of stay and family.",
                 desc="Moving to Sweden: the right order for Migrationsverket, Skatteverket, personnummer, ID card, bank account, BankID and Försäkringskassan — for EU, Nordic and non-EU citizens.")),
    dict(color="e",
         de=dict(slug="fixkosten-goeteborg", src="fixkosten-goeteborg.html", kick="Leben in Göteborg",
                 title="Fixkosten Göteborg",
                 card="Förskola nach Maxtaxa, Västtrafik, die Gesundheitsdeckel — was ein Haushalt in Göteborg im Monat fest zahlt, in Kronen und Euro.",
                 desc="Monatliche Fixkosten in Göteborg berechnen: Förskola-Gebühr nach Maxtaxa (ab Juli 2026), Västtrafik Zone A, Frikort und Högkostnadsskydd. Mit Euro-Umrechnung."),
         en=dict(slug="fixed-costs-gothenburg", src="en/fixed-costs-gothenburg.html", kick="Living in Gothenburg",
                 title="Fixed costs in Gothenburg",
                 card="Preschool fees, Västtrafik, the caps on healthcare costs — what a household in Gothenburg pays every month, in kronor and euros.",
                 desc="Calculate monthly fixed costs in Gothenburg: preschool fees (from July 2026), Västtrafik zone A, healthcare and medicine caps. With euro conversion.")),
    dict(color="f", data="kommunpreise.js",
         de=dict(slug="hauspreise-kommunen", src="hauspreise-kommunen.html", kick="Immobilien",
                 title="Hauspreise je Kommune",
                 card="Durchschnittspreise für Häuser und Ferienhäuser in allen 290 Kommunen, aus den amtlichen SCB-Zahlen — mit der Entwicklung seit 2020 und der Zahl der Verkäufe.",
                 desc="Durchschnittliche Hauspreise in Schweden je Kommune: alle 290 Kommunen mit Mittelwert, Veränderung seit 2020 und Anzahl der Verkäufe. Wohnhaus und Ferienhaus getrennt, in Kronen und Euro. Quelle SCB."),
         en=dict(slug="house-prices-municipalities", src="en/house-prices-municipalities.html", kick="Property",
                 title="House prices by municipality",
                 card="Average prices for houses and holiday houses in all 290 municipalities, from official SCB figures — with the change since 2020 and the number of sales.",
                 desc="Average house prices in Sweden by municipality: all 290 municipalities with the mean price, change since 2020 and number of sales. Year-round and holiday houses shown separately, in kronor and euros. Source: SCB.")),
]

PREFIX = {"de": "/", "en": "/en/"}


def url(lang, slug=None):
    return PREFIX[lang] + (slug + "/" if slug else "")


T = {  # Texte für Kopf, Fuß, Übersicht — je Sprache
    "de": dict(
        html_lang="de", og_locale="de_DE", suffix="Werkzeuge von nordabenteuer.de", mark="Werkzeuge", menu="Menü",
        nav=[(MAIN + "/", "Home"), (MAIN + "/ratgeber", "Ratgeber"), ("/", "Werkzeuge"), (MAIN + "/immobilien", "Immobilien"),
             (MAIN + "/shop", "Guides"), (MAIN + "/beratung", "Beratung"), (MAIN + "/about", "Über mich"), (MAIN + "/kontakt", "Kontakt")],
        nav_label="Hauptnavigation", switch="EN", switch_label="This tool in English",
        more="Weitere Werkzeuge", open="Öffnen",
        foot_claim="Der deutschsprachige Ratgeber für den Umzug nach Schweden und den Hauskauf dort — von jemandem, der beides gemacht hat.",
        foot_btn=(MAIN + "/beratung", "Konkrete Fragen? Reden wir."),
        foot_tools="Werkzeuge", foot_site="nordabenteuer.de",
        foot_links=[(MAIN + "/ratgeber", "Ratgeber — alle Artikel"), (MAIN + "/shop", "Guides zum Download"),
                    (MAIN + "/beratung", "Beratung und Objektcheck"), (MAIN + "/umzugscheck", "Kostenloser Umzugscheck"), (MAIN + "/kontakt", "Kontakt")],
        foot_legal="Alle Werkzeuge rechnen im Browser. Nichts wird gespeichert, hochgeladen oder von fremden Seiten abgerufen. Keine Rechts- oder Steuerberatung.",
        imprint="Impressum", privacy="Datenschutz",
        idx_title="Werkzeuge – nordabenteuer.de",
        idx_desc="Sechs kostenlose Werkzeuge für den Umzug nach Schweden und den Hauskauf dort: Inserat auf Deutsch, Kaufnebenkosten, Hauspreise je Kommune, Fragen an den Mäklare, Behörden-Reihenfolge, Fixkosten Göteborg. Alles rechnet im Browser.",
        idx_h1="Werkzeuge für Schweden, auf Deutsch.",
        idx_lede="Kleine Rechner und Listen für die Momente, in denen ein Artikel nicht reicht: wenn ein Inserat vor dir liegt, ein Gebot ansteht oder die Behördenkette anfängt. Kostenlos, ohne Anmeldung, ohne dass etwas deinen Browser verlässt.",
        idx_how="Wie diese Seiten arbeiten",
        idx_how1="Alles rechnet in deinem Browser. Es wird nichts hochgeladen, nichts gespeichert und keine fremde Website abgerufen — auch kein Immobilienportal. Du kopierst Text hinein, die Seite liest ihn, fertig.",
        idx_how2=f'Jedes Werkzeug trägt Zahlen, die sich jährlich ändern (Stämpelskatt, Maxtaxa, Patientavgifter). Der Stand steht jeweils unten auf der Seite. Wenn eine Zahl nicht mehr stimmt: <a href="{MAIN}/kontakt">kurz Bescheid sagen</a>.',
        idx_about=f'Die Werkzeuge gehören zu <a href="{MAIN}/">nordabenteuer.de</a>, dem deutschsprachigen Ratgeber für den Umzug nach Schweden und den Hauskauf dort. Die Erklärungen stammen aus den <a href="{MAIN}/ratgeber">Artikeln</a>; wo ein Werkzeug aufhört, fängt die <a href="{MAIN}/beratung">Beratung</a> an.',
    ),
    "en": dict(
        html_lang="en", og_locale="en_GB", suffix="Tools by nordabenteuer.de", mark="Tools", menu="Menu",
        nav=[(MAIN + "/english/welcome", "Home"), (MAIN + "/english/articles", "Articles"), ("/en/", "Tools"),
             (MAIN + "/english/real-estate", "Real Estate"), (MAIN + "/english/consulting", "Consulting"),
             (MAIN + "/english/about-me", "About"), (MAIN + "/english/contact", "Contact")],
        nav_label="Main navigation", switch="DE", switch_label="Dieses Werkzeug auf Deutsch",
        more="More tools", open="Open",
        foot_claim="A guide to moving to Sweden and buying a home there — from someone who has done both.",
        foot_btn=(MAIN + "/english/consulting", "Specific questions? Let’s talk."),
        foot_tools="Tools", foot_site="nordabenteuer.de",
        foot_links=[(MAIN + "/english/articles", "Articles — all guides"), (MAIN + "/english/real-estate", "Buying property in Sweden"),
                    (MAIN + "/english/consulting", "Consulting and property check"), (MAIN + "/english/contact", "Contact")],
        foot_legal="All tools calculate in your browser. Nothing is stored, uploaded or fetched from other websites. Not legal or tax advice.",
        imprint="Legal notice", privacy="Privacy",
        idx_title="Tools for moving to Sweden – nordabenteuer.de",
        idx_desc="Six free tools for moving to Sweden and buying a home there: read a Swedish listing, buying costs, house prices by municipality, questions for the estate agent, the order of Swedish authorities, fixed costs in Gothenburg. Everything runs in your browser.",
        idx_h1="Tools for Sweden, in English.",
        idx_lede="Small calculators and checklists for the moments when an article isn’t enough: when a listing is in front of you, a bid is coming up, or the paperwork begins. Free, no sign-up, and nothing leaves your browser.",
        idx_how="How these pages work",
        idx_how1="Everything is calculated in your browser. Nothing is uploaded, nothing is stored, and no other website is contacted — no property portal either. You paste text in, the page reads it, done.",
        idx_how2=f'Each tool uses figures that change every year (stamp duty, preschool fees, patient fees). The date is shown at the bottom of each page. If a number is out of date: <a href="{MAIN}/english/contact">let me know</a>.',
        idx_about=f'These tools are part of <a href="{MAIN}/english/welcome">nordabenteuer.de</a>, a guide to moving to Sweden and buying a home there. The explanations come from the <a href="{MAIN}/english/articles">articles</a>; where a tool stops, <a href="{MAIN}/english/consulting">consulting</a> takes over.',
    ),
}

FONTS = ('<link rel="preload" href="/assets/fonts/dm-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>'
         '<link rel="preload" href="/assets/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>')


def head(lang, title, desc, path, alternates=None, extra=""):
    t = T[lang]
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{HOST}{p}">\n' for l, p in alternates.items())
        alt += f'<link rel="alternate" hreflang="x-default" href="{HOST}{alternates["de"]}">\n'
    return f"""<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{HOST}{path}">
{alt}<meta property="og:type" content="website">
<meta property="og:site_name" content="nordabenteuer.de">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{HOST}{path}">
<meta property="og:locale" content="{t['og_locale']}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#FFF6E6">
{FONTS}
<link rel="stylesheet" href="/assets/nab.css?v={CSSV}">
<script src="/assets/zahlen.js?v={ZAHLENV}"></script>
{extra}
</head>
<body>"""


def header(lang, switch_href):
    """Gleiche Navigation wie die jeweilige Sprachfassung von www.nordabenteuer.de; Werkzeuge markiert."""
    t = T[lang]
    here = PREFIX[lang]
    links = "\n    ".join(
        f'<a href="{h}"' + (' aria-current="page"' if h == here else '') + f'>{l}</a>' for h, l in t["nav"])
    other = "en" if lang == "de" else "de"
    home = t["nav"][0][0]
    return f"""<div class="nab-head"><div class="in">
  <a class="nab-mark" href="{home}" aria-label="nordabenteuer.de">nordabenteuer<b>.</b> <small>{t['mark']}</small></a>
  <button class="nab-burger" type="button" aria-expanded="false" aria-controls="nab-nav"><span></span>{t['menu']}</button>
  <nav class="nab-nav" id="nab-nav" aria-label="{t['nav_label']}">
    {links}
    <a class="nab-lang" href="{switch_href}" lang="{other}" hreflang="{other}" aria-label="{t['switch_label']}">{t['switch']}</a>
  </nav>
</div></div>
<script>(function(){{var d=document.documentElement;d.className+=' js';var b=document.querySelector('.nab-burger'),n=document.getElementById('nab-nav');b.addEventListener('click',function(){{var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));n.classList.toggle('open',!o);}});}})();</script>"""


def more(lang, current_slug):
    t = T[lang]
    items = "".join(f'<li><a href="{url(lang, x[lang]["slug"])}">{x[lang]["title"]}</a></li>' for x in TOOLS if x[lang]["slug"] != current_slug)
    return f"""<div class="nab-more"><div class="in">
  <h2>{t['more']}</h2>
  <ul>{items}</ul>
</div></div>"""


def footer(lang):
    t = T[lang]
    tools = "".join(f'<li><a href="{url(lang, x[lang]["slug"])}">{x[lang]["title"]}</a></li>' for x in TOOLS)
    site = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in t["foot_links"])
    return f"""<div class="nab-foot"><div class="in">
  <div>
    <p class="mark">nordabenteuer<b>.</b></p>
    <p>{t['foot_claim']}</p>
    <a class="btn" href="{t['foot_btn'][0]}">{t['foot_btn'][1]}</a>
  </div>
  <div>
    <h3>{t['foot_tools']}</h3>
    <ul>{tools}</ul>
  </div>
  <div>
    <h3>{t['foot_site']}</h3>
    <ul>{site}</ul>
  </div>
  <div class="legal">
    <span>{t['foot_legal']}</span>
    <span><a href="{MAIN}/impressum">{t['imprint']}</a> · <a href="{MAIN}/datenschutz">{t['privacy']}</a> · © {TODAY[:4]} Sebastian Schiefner</span>
  </div>
</div></div>
<script>(function(){{var s=(window.NAB_ZAHLEN||{{}}).stand;if(!s)return;document.querySelectorAll('[data-stand]').forEach(function(e){{e.textContent=s['{lang}'];}});}})();</script>
</body>
</html>"""


def tool_body(src_text):
    """Entfernt Titel/Meta/Fonts und die Farb-Tokens; Rest (Stil, Markup, Skript) bleibt."""
    lines = src_text.split("\n")
    # erste drei Zeilen: <title>, <meta claude:…>, Google-Fonts-Link (wird verworfen)
    assert lines[0].startswith("<title>") and lines[2].startswith("<link"), "unerwarteter Dateikopf"
    text = "\n".join(lines[3:])
    text = re.sub(r":root\{.*?\n\}\n", "", text, count=1, flags=re.S)
    text = re.sub(r"@media \(prefers-color-scheme:dark\)\{:root:not\(\[data-theme=\"light\"\]\)\{.*?color-scheme:dark;?\}\}\n", "", text, count=1, flags=re.S)
    text = re.sub(r":root\[data-theme=\"dark\"\]\{.*?color-scheme:dark;?\}\n", "", text, count=1, flags=re.S)
    text = text.replace("*{box-sizing:border-box}\n", "", 1)
    text = re.sub(r"^body\{[^\n]*\}\n", "", text, count=1, flags=re.M)
    assert ":root" not in text and "prefers-color-scheme" not in text
    # Elementselektoren der Werkzeuge auf <main> begrenzen, damit sie Kopf- und Fußleiste nicht treffen
    text = re.sub(r"^(header|footer|h1|h2|button|textarea)(?=[{:,\s])", r"main \1", text, flags=re.M)
    text = re.sub(r"^(input\[type=number\],select)", r"main input[type=number],main select", text, flags=re.M)
    text = text.replace("main textarea:focus-visible,button:focus-visible", "main textarea:focus-visible,main button:focus-visible")
    text = text.replace("input:focus-visible,select:focus-visible,button:focus-visible", "main input:focus-visible,main select:focus-visible,main button:focus-visible")
    text = text.replace("main h1{font-family:var(--font-display);font-weight:600", "main h1{font-family:var(--font-display);font-weight:800")
    return text


def build_tool(tool, lang):
    x = tool[lang]
    other = "en" if lang == "de" else "de"
    path = url(lang, x["slug"])
    alternates = {"de": url("de", tool["de"]["slug"]), "en": url("en", tool["en"]["slug"])}
    body = tool_body((SRC / x["src"]).read_text(encoding="utf-8"))
    title = f'{x["title"]} – {T[lang]["suffix"]}'
    jsonld = {
        "@context": "https://schema.org", "@type": "WebApplication",
        "name": x["title"], "url": HOST + path, "description": x["desc"],
        "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": lang,
        "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "publisher": {"@type": "Organization", "name": "nordabenteuer.de", "url": MAIN + "/"},
        "author": {"@type": "Person", "name": "Sebastian Schiefner"},
    }
    extra = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    if tool.get("data"):  # zusaetzliche Datendatei, nur fuer dieses Werkzeug
        extra += '<script src="/assets/' + tool['data'] + '?v=' + KOMMUNV + '"></script>'
    html = (head(lang, title, x["desc"], path, alternates, extra)
            + header(lang, alternates[other])
            + "\n<main>\n" + body + "\n</main>\n"
            + more(lang, x["slug"]) + footer(lang))
    d = OUT / path.strip("/"); d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def build_index(lang):
    t = T[lang]
    other = "en" if lang == "de" else "de"
    cards = "".join(f"""
    <li><a class="nab-card {x['color']}" href="{url(lang, x[lang]['slug'])}">
      <span class="kick">{x[lang]['kick']}</span>
      <h2>{x[lang]['title']}</h2>
      <p>{x[lang]['card']}</p>
      <span class="go">{t['open']}</span>
    </a></li>""" for x in TOOLS)
    alternates = {"de": "/", "en": "/en/"}
    html = head(lang, t["idx_title"], t["idx_desc"], PREFIX[lang], alternates) + header(lang, alternates[other]) + f"""
<main class="nab-index">
  <h1>{t['idx_h1']}</h1>
  <p class="lede">{t['idx_lede']}</p>
  <ul class="nab-grid">{cards}
  </ul>
  <div class="nab-promise">
    <strong>{t['idx_how']}</strong>
    <span>{t['idx_how1']}</span>
    <span>{t['idx_how2']}</span>
  </div>
  <p class="nab-about">{t['idx_about']}</p>
</main>
""" + footer(lang)
    d = OUT / PREFIX[lang].strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def build_404():
    de = "".join(f'<li><a href="{url("de", x["de"]["slug"])}">{x["de"]["title"]}</a></li>' for x in TOOLS)
    en = "".join(f'<li><a href="{url("en", x["en"]["slug"])}">{x["en"]["title"]}</a></li>' for x in TOOLS)
    html = head("de", "Seite nicht gefunden · Page not found – nordabenteuer.de", "Diese Seite gibt es nicht.", "/404.html",
                extra='<meta name="robots" content="noindex">') + header("de", "/en/") + f"""
<main class="nab-404">
  <h1>Hier ist nichts.</h1>
  <p>Die Adresse führt zu keinem Werkzeug. Hier sind alle fünf:</p>
  <ul>{de}</ul>
  <h2 lang="en">Nothing here.</h2>
  <p lang="en">This address doesn’t lead to a tool. Here are all five in English:</p>
  <ul lang="en">{en}</ul>
  <p>Oder zurück zu <a href="{MAIN}/">nordabenteuer.de</a> · <a lang="en" href="{MAIN}/english/welcome">back to nordabenteuer.de</a></p>
</main>
""" + footer("de")
    (OUT / "404.html").write_text(html, encoding="utf-8")


def build_meta():
    pairs = [({"de": "/", "en": "/en/"}, "1.0")] + [
        ({"de": url("de", x["de"]["slug"]), "en": url("en", x["en"]["slug"])}, "0.8") for x in TOOLS]
    rows = []
    for alt, prio in pairs:
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{HOST}{p}"/>' for l, p in alt.items())
        for l, p in alt.items():
            rows.append(f"  <url><loc>{HOST}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority>{links}</url>\n")
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "".join(rows) + "</urlset>\n")
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {HOST}/sitemap.xml\n", encoding="utf-8")
    (OUT / "CNAME").write_text("werkzeuge.nordabenteuer.de\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ASSETS, OUT / "assets", dirs_exist_ok=True)
    for tool in TOOLS:
        for lang in ("de", "en"):
            build_tool(tool, lang)
    for lang in ("de", "en"):
        build_index(lang)
    build_404()
    build_meta()
    print("gebaut:", len(TOOLS), "Werkzeuge × 2 Sprachen + 2 Übersichten, 404, sitemap (mit hreflang), robots, CNAME")


if __name__ == "__main__":
    main()
