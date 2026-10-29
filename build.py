#!/usr/bin/env python3
"""Baut werkzeuge.nordabenteuer.de aus src/*.html nach docs/.

Jede Datei in src/ ist ein eigenständiges Werkzeug (Stil, Markup, Skript) ohne
<html>/<head>. Dieses Skript legt Kopfleiste, Fußleiste, Meta-Daten und die
gemeinsame Gestaltung (assets/nab.css) darum und schreibt docs/<slug>/index.html.

    python3 build.py

Danach docs/ committen — GitHub Pages liefert den Ordner aus.
"""
import re, shutil, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC, OUT, ASSETS = ROOT / "src", ROOT / "docs", ROOT / "assets"
HOST = "https://werkzeuge.nordabenteuer.de"
MAIN = "https://www.nordabenteuer.de"
TODAY = datetime.date.today().isoformat()

TOOLS = [
    dict(slug="inserat-auf-deutsch", src="inserat-auf-deutsch.html", color="a",
         kick="Immobilien",
         title="Inserat auf Deutsch",
         card="Faktenliste eines schwedischen Inserats einfügen — jede Zeile erklärt, dazu Preis je m², Avgift im Jahr und die Stämpelskatt, die im Inserat fehlt.",
         desc="Schwedisches Immobilieninserat verstehen: Utgångspris, Avgift, Boarea, Driftkostnad auf Deutsch erklärt und die fehlenden Zahlen ausgerechnet. Läuft im Browser, nichts wird hochgeladen."),
    dict(slug="kaufnebenkosten", src="kaufnebenkosten-schweden.html", color="b",
         kick="Immobilien",
         title="Kaufnebenkosten Schweden",
         card="Stämpelskatt, Pantbrev, Gebühren und die jährliche Fastighetsavgift — was beim Hauskauf in Schweden zum Kaufpreis dazukommt.",
         desc="Kaufnebenkosten beim Hauskauf in Schweden berechnen: Stämpelskatt 1,5 %, Pantbrev 2 %, Lagfart-Gebühr, Fastighetsavgift. Mit Bostadsrätt, Äganderätt und Tomträtt."),
    dict(slug="fragen-an-den-maeklare", src="fragen-an-den-maeklare.html", color="c",
         kick="Besichtigung",
         title="Fragen an den Mäklare",
         card="48 Fragen für die Visning, nach Objektart sortiert — jede auf Schwedisch und Deutsch, zum Kopieren.",
         desc="Fragen an den Mäklare bei der Besichtigung in Schweden: Bostadsrätt, Haus oder Ferienhaus. Schwedischer Wortlaut mit deutscher Übersetzung, als Liste zum Mitnehmen."),
    dict(slug="behoerden-reihenfolge", src="behoerden-reihenfolge.html", color="d",
         kick="Umzug",
         title="Behörden-Reihenfolge Schweden",
         card="Personnummer, ID-kort, Bankkonto, BankID — in welcher Reihenfolge, und was wovon abhängt. Nach Dauer, Status und Kindern.",
         desc="Behördengänge nach dem Umzug nach Schweden in der richtigen Reihenfolge: Skatteverket, Personnummer, ID-kort, Bankkonto, BankID, Försäkringskassan — angepasst an deine Lage."),
    dict(slug="fixkosten-goeteborg", src="fixkosten-goeteborg.html", color="e",
         kick="Leben in Göteborg",
         title="Fixkosten Göteborg",
         card="Förskola nach Maxtaxa, Västtrafik, die Gesundheitsdeckel — was ein Haushalt in Göteborg im Monat fest zahlt, in Kronen und Euro.",
         desc="Monatliche Fixkosten in Göteborg berechnen: Förskola-Gebühr nach Maxtaxa (ab Juli 2026), Västtrafik Zone A, Frikort und Högkostnadsskydd. Mit Euro-Umrechnung."),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap">')


def head(title, desc, path, extra=""):
    url = HOST + path
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="nordabenteuer.de">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="de_DE">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#FFF6E6">
{FONTS}
<link rel="stylesheet" href="/assets/nab.css">
{extra}
</head>
<body>"""


def header(current=None):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<div class="nab-head"><div class="in">
  <a class="nab-mark" href="{MAIN}/" aria-label="nordabenteuer.de">nordabenteuer<b>.</b> <small>Werkzeuge</small></a>
  <nav class="nab-nav" aria-label="Seiten">
    {a('/', 'Alle Werkzeuge', 'index')}
    {a(MAIN + '/ratgeber', 'Ratgeber', 'ratgeber')}
    {a(MAIN + '/shop', 'Guides', 'shop')}
    {a(MAIN + '/beratung', 'Beratung', 'beratung')}
  </nav>
</div></div>"""


def more(current_slug):
    items = "".join(f'<li><a href="/{t["slug"]}/">{t["title"]}</a></li>' for t in TOOLS if t["slug"] != current_slug)
    return f"""<div class="nab-more"><div class="in">
  <h2>Weitere Werkzeuge</h2>
  <ul>{items}</ul>
</div></div>"""


def footer():
    tools = "".join(f'<li><a href="/{t["slug"]}/">{t["title"]}</a></li>' for t in TOOLS)
    return f"""<div class="nab-foot"><div class="in">
  <div>
    <p class="mark">nordabenteuer<b>.</b></p>
    <p>Der deutschsprachige Ratgeber für den Umzug nach Schweden und den Hauskauf dort — von jemandem, der beides gemacht hat.</p>
    <a class="btn" href="{MAIN}/beratung">Konkrete Fragen? Reden wir.</a>
  </div>
  <div>
    <h3>Werkzeuge</h3>
    <ul>{tools}</ul>
  </div>
  <div>
    <h3>nordabenteuer.de</h3>
    <ul>
      <li><a href="{MAIN}/ratgeber">Ratgeber — alle Artikel</a></li>
      <li><a href="{MAIN}/shop">Guides zum Download</a></li>
      <li><a href="{MAIN}/beratung">Beratung und Objektcheck</a></li>
      <li><a href="{MAIN}/umzugscheck">Kostenloser Umzugscheck</a></li>
      <li><a href="{MAIN}/kontakt">Kontakt</a></li>
    </ul>
  </div>
  <div class="legal">
    <span>Alle Werkzeuge rechnen im Browser. Nichts wird gespeichert, hochgeladen oder von fremden Seiten abgerufen. Keine Rechts- oder Steuerberatung.</span>
    <span><a href="{MAIN}/impressum">Impressum</a> · <a href="{MAIN}/datenschutz">Datenschutz</a> · © {TODAY[:4]} Sebastian Schiefner</span>
  </div>
</div></div>
</body>
</html>"""


def tool_body(src_text):
    """Entfernt Titel/Meta/Fonts und die Farb-Tokens; Rest (Stil, Markup, Skript) bleibt."""
    lines = src_text.split("\n")
    # erste drei Zeilen: <title>, <meta claude:…>, Google-Fonts-Link
    assert lines[0].startswith("<title>") and lines[2].startswith("<link"), "unerwarteter Dateikopf"
    text = "\n".join(lines[3:])
    # :root{…} (mehrzeilig) entfernen
    text = re.sub(r":root\{.*?\n\}\n", "", text, count=1, flags=re.S)
    # Dark-Mode-Blöcke entfernen (ein- oder mehrzeilig)
    text = re.sub(r"@media \(prefers-color-scheme:dark\)\{:root:not\(\[data-theme=\"light\"\]\)\{.*?color-scheme:dark;?\}\}\n", "", text, count=1, flags=re.S)
    text = re.sub(r":root\[data-theme=\"dark\"\]\{.*?color-scheme:dark;?\}\n", "", text, count=1, flags=re.S)
    # Grundregeln, die nab.css übernimmt
    text = text.replace("*{box-sizing:border-box}\n", "", 1)
    text = re.sub(r"^body\{[^\n]*\}\n", "", text, count=1, flags=re.M)
    assert ":root" not in text and "prefers-color-scheme" not in text
    # Eigenständige Elementselektoren der Werkzeuge auf <main> begrenzen, damit sie Kopf- und Fußleiste nicht treffen
    text = re.sub(r"^(header|footer|h1|h2|button|textarea)(?=[{:,\s])", r"main \1", text, flags=re.M)
    text = re.sub(r"^(input\[type=number\],select)", r"main input[type=number],main select", text, flags=re.M)
    text = text.replace("main textarea:focus-visible,button:focus-visible", "main textarea:focus-visible,main button:focus-visible")
    text = text.replace("input:focus-visible,select:focus-visible,button:focus-visible", "main input:focus-visible,main select:focus-visible,main button:focus-visible")
    text = text.replace("main h1{font-family:var(--font-display);font-weight:600", "main h1{font-family:var(--font-display);font-weight:800")
    return text


def build_tool(t):
    src = (SRC / t["src"]).read_text(encoding="utf-8")
    body = tool_body(src)
    title = f'{t["title"]} – Werkzeuge von nordabenteuer.de'
    jsonld = {
        "@context": "https://schema.org", "@type": "WebApplication",
        "name": t["title"], "url": f'{HOST}/{t["slug"]}/', "description": t["desc"],
        "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": "de",
        "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "publisher": {"@type": "Organization", "name": "nordabenteuer.de", "url": MAIN + "/"},
        "author": {"@type": "Person", "name": "Sebastian Schiefner"},
    }
    import json
    extra = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    html = (head(title, t["desc"], f'/{t["slug"]}/', extra)
            + header()
            + "\n<main>\n" + body + "\n</main>\n"
            + more(t["slug"]) + footer())
    d = OUT / t["slug"]; d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def build_index():
    cards = "".join(f"""
    <li><a class="nab-card {t['color']}" href="/{t['slug']}/">
      <span class="kick">{t['kick']}</span>
      <h2>{t['title']}</h2>
      <p>{t['card']}</p>
      <span class="go">Öffnen</span>
    </a></li>""" for t in TOOLS)
    title = "Werkzeuge – nordabenteuer.de"
    desc = "Fünf kostenlose Werkzeuge für den Umzug nach Schweden und den Hauskauf dort: Inserat auf Deutsch, Kaufnebenkosten, Fragen an den Mäklare, Behörden-Reihenfolge, Fixkosten Göteborg. Alles rechnet im Browser."
    html = head(title, desc, "/") + header("index") + f"""
<main class="nab-index">
  <h1>Werkzeuge für Schweden, auf Deutsch.</h1>
  <p class="lede">Kleine Rechner und Listen für die Momente, in denen ein Artikel nicht reicht: wenn ein Inserat vor dir liegt, ein Gebot ansteht oder die Behördenkette anfängt. Kostenlos, ohne Anmeldung, ohne dass etwas deinen Browser verlässt.</p>
  <ul class="nab-grid">{cards}
  </ul>
  <div class="nab-promise">
    <strong>Wie diese Seiten arbeiten</strong>
    <span>Alles rechnet in deinem Browser. Es wird nichts hochgeladen, nichts gespeichert und keine fremde Website abgerufen — auch kein Immobilienportal. Du kopierst Text hinein, die Seite liest ihn, fertig.</span>
    <span>Jedes Werkzeug trägt Zahlen, die sich jährlich ändern (Stämpelskatt, Maxtaxa, Patientavgifter). Der Stand steht jeweils unten auf der Seite. Wenn eine Zahl nicht mehr stimmt: <a href="{MAIN}/kontakt">kurz Bescheid sagen</a>.</span>
  </div>
  <p class="nab-about">Die Werkzeuge gehören zu <a href="{MAIN}/">nordabenteuer.de</a>, dem deutschsprachigen Ratgeber für den Umzug nach Schweden und den Hauskauf dort. Die Erklärungen stammen aus den <a href="{MAIN}/ratgeber">Artikeln</a>; wo ein Werkzeug aufhört, fängt die <a href="{MAIN}/beratung">Beratung</a> an.</p>
</main>
""" + footer()
    (OUT / "index.html").write_text(html, encoding="utf-8")


def build_404():
    html = head("Seite nicht gefunden – Werkzeuge von nordabenteuer.de", "Diese Seite gibt es nicht.", "/404.html",
                '<meta name="robots" content="noindex">') + header() + f"""
<main class="nab-404">
  <h1>Hier ist nichts.</h1>
  <p>Die Adresse führt zu keinem Werkzeug. Vielleicht hat sich die Schreibweise geändert — hier sind alle fünf:</p>
  <ul>{"".join(f'<li><a href="/{t["slug"]}/">{t["title"]}</a></li>' for t in TOOLS)}</ul>
  <p>Oder zurück zu <a href="{MAIN}/">nordabenteuer.de</a>.</p>
</main>
""" + footer()
    (OUT / "404.html").write_text(html, encoding="utf-8")


def build_meta():
    urls = [("/", "1.0")] + [(f'/{t["slug"]}/', "0.8") for t in TOOLS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{HOST}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in urls) + "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {HOST}/sitemap.xml\n", encoding="utf-8")
    (OUT / "CNAME").write_text("werkzeuge.nordabenteuer.de\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ASSETS, OUT / "assets")
    for t in TOOLS:
        build_tool(t)
    build_index()
    build_404()
    build_meta()
    print("gebaut:", ", ".join(t["slug"] for t in TOOLS), "+ index, 404, sitemap, robots, CNAME")


if __name__ == "__main__":
    main()
