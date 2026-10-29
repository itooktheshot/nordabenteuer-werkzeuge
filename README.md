# werkzeuge.nordabenteuer.de

Statische Website mit den Web-Werkzeugen von nordabenteuer.de. Gehostet auf
GitHub Pages, weil der Squarespace-Tarif kein JavaScript in Code-Blöcken erlaubt.

## Aufbau

| Ordner / Datei | Zweck |
|---|---|
| `src/*.html` | Die Werkzeuge selbst — je eine Datei mit `<style>`, Markup und `<script>`, ohne `<html>`/`<head>`. **Hier wird geändert.** |
| `assets/nab.css` | Gemeinsame Gestaltung: Marken-Tokens (Pastellpop, wie auf nordabenteuer.de), Kopf- und Fußleiste, Übersicht. |
| `assets/favicon.svg` | Favicon (Kobalt-Quadrat, cremefarbenes n, Zitronenpunkt). |
| `build.py` | Baut aus `src/` und `assets/` den Ordner `docs/` — Seiten, Übersicht, 404, Sitemap, robots.txt, CNAME. |
| `docs/` | **Generiert.** Das, was GitHub Pages ausliefert. Nicht von Hand bearbeiten. |

## Ändern und veröffentlichen

```
python3 build.py
git add -A && git commit -m "…" && git push
```

GitHub Pages ist auf `main` / Ordner `docs` eingestellt. Nach dem Push dauert
es ein bis zwei Minuten.

Neues Werkzeug: Datei nach `src/` legen (gleicher Aufbau wie die anderen: erste
Zeile `<title>`, zweite `<meta>`, dritte Fonts-Link, dann `<style>`, Markup,
`<script>`), Eintrag in `TOOLS` in `build.py`, bauen.

## Die fünf Werkzeuge

| Adresse | Datei | Hängt an |
|---|---|---|
| `/inserat-auf-deutsch/` | `inserat-auf-deutsch.html` | Objektcheck 149 € |
| `/kaufnebenkosten/` | `kaufnebenkosten-schweden.html` | Objektcheck 149 € |
| `/fragen-an-den-maeklare/` | `fragen-an-den-maeklare.html` | Objektcheck 149 € |
| `/behoerden-reihenfolge/` | `behoerden-reihenfolge.html` | Erstgespräch, 50 €/h |
| `/fixkosten-goeteborg/` | `fixkosten-goeteborg.html` | Erstgespräch |

## Wartung — die Zahlen

Alle veränderlichen Werte stehen je Datei in **einem** Objekt oben im `<script>`
(`SATS`, `T`). Stand 29.10.2026, alle gegen die Primärquelle geprüft:

| Wert | Datei | Quelle | Prüfen |
|---|---|---|---|
| Stämpelskatt 1,5 % · Pantbrev 2 % · 825 kr · 375 kr | kaufnebenkosten | Lantmäteriet | jährlich |
| Fastighetsavgift 0,75 %, Deckel 10.425 kr | kaufnebenkosten | Skatteverket, Belopp och procent 2026 | jährlich, Januar |
| Maxtaxa: Fribelopp 10.000, Inkomsttak 51.560, 3/2/1 % bzw. 2/1/1 % ab 3 J., Deckel 1.547/1.031/516 | fixkosten | Göteborgs Stads avgifter för förskola, gültig ab 1.7.2026 (Jul–Dez „preliminärt“) | **1. Juli 2027**, und sobald die Stadt die vorläufigen Beträge bestätigt |
| Västtrafik Zone A: 305 kr bis 2.12.2026, danach 750 kr (Göteborg-Tarif); 890 kr ohne Göteborg-Anmeldung | fixkosten | vasttrafik.se | **Datumsschalter in `T.aktionEnde`** — stellt am 3.12. selbst um; Preis 2027 prüfen |
| Vårdcentral 200 · Sjuksköterska 50 · Specialist 300 · Akuten 400 · Frikort 1.450 | fixkosten | 1177 Västra Götaland | jährlich, Januar |
| Läkemedel-Högkostnadsskydd 3.800 | fixkosten | 1177/TLV, seit Juli 2026 | jährlich |
| EUR/SEK 11,12 | fixkosten | nur Größenordnung | gelegentlich |
| Besiktning 9.600–10.800 kr | fragen-an-den-maeklare (Hinweistext) | Anticimex | jährlich |

Besser wäre, die Werkzeuge aus `tools/guides/facts.py` zu speisen — nicht
gebaut, nur vorgeschlagen.

## Zwei Entwurfsentscheidungen

**Kein Link-Abruf.** Hemnet ist börsennotiert, seine Daten sind das Produkt;
automatisiertes Auslesen zieht eine Unterlassungsaufforderung nach sich. Abrufen
hieße außerdem Server, Kosten, Verarbeitung fremder Wohnungssuchen. Eingefügter
Text erledigt beides. Alle Werkzeuge laufen vollständig im Browser des Besuchers.

**Markenlinie.** „Hemnet“ steht beschreibend in Texten, in keinem Produktnamen,
Seitentitel oder Pfad. Keine Nachahmung ihrer Gestaltung.

## Datenschutz

Die Seiten setzen keine Cookies, laden kein Analytics und senden nichts. Die
Schriften (Bricolage Grotesque, DM Sans, DM Mono) liegen selbst gehostet in
`assets/fonts/` (Fontsource, SIL Open Font License) — es gibt **keine**
Verbindung zu Google Fonts. Einziger Dritter ist GitHub als Hoster
(Server-Logs); das steht in der Datenschutzerklärung von nordabenteuer.de,
Abschnitt 3.

Die Zeile 3 in jeder `src/*.html` (Google-Fonts-Link) wird von `build.py`
verworfen und landet nicht in `docs/`.
