import csv, io, json, datetime, sys
src, out = sys.argv[1], sys.argv[2]
rows = list(csv.reader(io.open(src, encoding="utf-8"), delimiter=";"))
def num(v):
    v = v.strip()
    if v in ("", "..", "...", "."): return None
    return int(v)
riket, lan, kom = None, {}, []
for r in rows:
    kod, namn = r[0].strip(), r[1].strip()
    n25, p25, p20, fn25, fp25 = (num(x) for x in r[2:7])
    rec = dict(namn=namn, n=n25, p=p25, p0=p20, fn=fn25, fp=fp25)
    if kod == "00": riket = rec
    elif len(kod) == 2: lan[kod] = rec
    else: kom.append([kod, namn, n25, p25, p20, fn25, fp25])
kom.sort(key=lambda x: x[1])
assert riket and len(lan) == 21 and len(kom) == 290, (bool(riket), len(lan), len(kom))
js = """/* werkzeuge.nordabenteuer.de — Hauspreise je Kommune. GENERIERT, nicht von Hand ändern.
 *
 * Quelle: SCB, Statistikdatabasen, Tabelle "Försålda småhus efter region (kommun,
 * län, riket) och fastighetstyp" (BO0501B / FastprisSHRegionAr), abgerufen am %(abruf)s.
 * SCB-Aktualisierung der Jahreswerte: jeweils Anfang Juni (letzte Aktualisierung
 * der Tabelle laut SCB: 05.06.2026). Nächster Datenstand also Juni 2027 mit dem Jahr 2026.
 *
 * Einheit aller Preise: tkr = Tausend Kronen, Mittelwert der Köpeskilling.
 * p  = Mittelwert 2025, p0 = Mittelwert 2020 (für den Fünfjahresvergleich),
 * n  = Anzahl verkaufter Objekte 2025. f* = dasselbe für fritidshus.
 * null heißt: SCB weist für diese Kommune keinen Wert aus (zu wenige Verkäufe).
 *
 * Neu holen: siehe README, Abschnitt "Hauspreise aktualisieren".
 */
window.NAB_KOMMUNPREISE = {
  jahr: 2025,
  vorjahr: 2020,
  abruf: %(abrufjson)s,
  stand: { de: "Daten f\\u00fcr 2025, abgerufen im November 2026", en: "2025 data, retrieved November 2026" },
  quelle: {
    name: "SCB, Statistikdatabasen (BO0501B, FastprisSHRegionAr)",
    url: "https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__BO__BO0501__BO0501B/FastprisSHRegionAr/",
    naechstesUpdate: { de: "Juni 2027 (Jahr 2026)", en: "June 2027 (2026 data)" }
  },
  riket: %(riket)s,
  lan: %(lan)s,
  kolumnen: ["kod", "namn", "n", "p", "p0", "fn", "fp"],
  kommuner: [
%(kom)s
  ]
};
""" % dict(
    abruf=datetime.date.today().strftime("%d.%m.%Y"),
    abrufjson=json.dumps(datetime.date.today().isoformat()),
    riket=json.dumps(riket, ensure_ascii=False),
    lan=json.dumps(lan, ensure_ascii=False, indent=4).replace("\n", "\n  "),
    kom="\n".join("    " + json.dumps(k, ensure_ascii=False) + "," for k in kom).rstrip(","),
)
io.open(out, "w", encoding="utf-8").write(js)
print("Kommunen:", len(kom), "| Län:", len(lan), "| Riket p:", riket["p"], "| Bytes:", len(js.encode()))
