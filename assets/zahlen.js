/* werkzeuge.nordabenteuer.de — ALLE veränderlichen Zahlen, für Deutsch und Englisch.
 *
 * Nur hier ändern. Jede deutsche und englische Werkzeugseite liest diese Datei.
 * Nach einer Änderung: `python3 build.py`, committen, pushen (der Build hängt
 * einen Versionsparameter an, Besucher bekommen die neue Fassung sofort).
 *
 * Geprüft am 29.10.2026 gegen die Primärquellen (siehe README, Tabelle „Wartung").
 */
window.NAB_ZAHLEN = {
  stand: { de: 'Oktober 2026', en: 'October 2026' },

  // Kauf — Lantmäteriet, Skatteverket
  kauf: {
    stampel: 0.015,            // Stämpelskatt Privatperson, auf den höheren Wert aus Kaufpreis und Taxeringsvärde
    pantbrev: 0.02,            // je neu ausgestelltem Pantbrev
    lagfartAvgift: 825,        // Expeditionsavgift Lagfart
    pantbrevAvgift: 375,       // Expeditionsavgift je Pantbrev
    fastighetsavgiftSats: 0.0075,
    fastighetsavgiftTak: 10425,
    fastighetsavgiftJahr: 2026 // Einkommensjahr des Deckels
  },

  // Besichtigung — Anticimex
  besiktning: { von: 9600, bis: 10800 },

  // Göteborg — Göteborgs Stad, Västtrafik, 1177 VGR, TLV
  goeteborg: {
    fribelopp: 10000,          // vom Bruttoeinkommen abgezogen, bevor der Prozentsatz greift
    inkomsttak: 51560,         // höchstes anrechenbares Einkommen im Monat (ab 1.7.2026, vorläufig)
    pct: { klein: [0.03, 0.02, 0.01], gross: [0.02, 0.01, 0.01] },  // jüngstes Kind zuerst; ab August des Jahres, in dem es 3 wird, eine Stufe niedriger
    tak: { klein: [1547, 1031, 516], gross: [1031, 516, 516] },     // Höchstbeträge Göteborg ab 1.7.2026
    vasttrafikGbgAktion: 305,  // Zone A, folkbokförd in Göteborg, halbiert bis 2.12.2026
    vasttrafikGbg: 750,        // Zone A, folkbokförd in Göteborg, regulär (Stadt zahlt 140 kr zu)
    vasttrafikAVoll: 890,      // Zone A ohne Göteborg-Rabatt
    aktionEnde: '2026-12-02',  // letzter Verkaufstag der halbierten 30-Tage-Karte
    vardcentral: 200, sjukskoterska: 50, specialist: 300, akuten: 400,
    frikort: 1450,             // Högkostnadsskydd Arztbesuche, 12 Monate
    lakemedel: 3800,           // Högkostnadsskydd Arzneimittel, 12 Monate (seit Juli 2026)
    eurkurs: 11.12             // nur Größenordnung
  }
};
