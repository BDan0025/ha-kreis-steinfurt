# Änderungsübersicht

## 0.6.1

- Fehler beim Erstellen der Kartenpunkte 1 bis 10 behoben. Die Punkte liefern nun korrekt Einsatzart, Details und Kartenposition.

## 0.6.0

- Neue Dashboard-Karte „Letzte 10 Einsätze“ mit laufenden und abgeschlossenen Einsätzen.
- Neue geografische Karte für die zehn neuesten Einsätze. Ihre Markierungen werden automatisch bei jedem neuen Einsatz aktualisiert.
- Ortskarte „letzter Einsatz“ im Dashboard und als Git-Vorlage auf die feste Orts-Entität umgestellt.
- Laufende Einsätze werden in der Ortskarte korrekt mit ihrer bisherigen Laufzeit dargestellt.

## 0.5.1

- Einstellungsseite vollständig und verständlich auf Deutsch beschriftet.
- Kurze Erklärungen zu jedem An-/Aus-Schalter ergänzt.
- GitHub-Dokumentation als Startseite mit Unterseiten neu strukturiert.

## 0.5.0

- Feste „Letzter Einsatz“-Entität für jeden ausgewählten Ort.
- Ortsübersichten für jeden ausgewählten Ort, auch ohne aktuell gespeicherten Einsatz.
- Schalter für einzelne Einsatz-Entities, Ortsübersichten, Orts-„letzter Einsatz“-Entities und Listenattribute.
- Dashboard-Beispiel für den letzten Einsatz eines Ortes auf die neue Entity umgestellt.
- Dokumentation in übersichtliche Unterseiten aufgeteilt.

## 0.4.1

- Entity-IDs der Zähler an die tatsächlich von Home Assistant vergebenen IDs angepasst.

## 0.4.0

- Abschlusszeit, Einsatzdauer und Zeit seit Abschluss ergänzt.
- Zeit seit Abschluss aktualisiert sich im Zehn-Minuten-Takt ohne weiteren Abruf der Quelle.
