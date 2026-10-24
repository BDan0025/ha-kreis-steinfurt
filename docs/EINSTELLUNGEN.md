# Einstellungen

Öffne **Einstellungen → Geräte & Dienste → Kreis Steinfurt Einsätze → Konfigurieren**. Jede Änderung lädt die Integration neu und wird anschließend für die Entity-Erzeugung verwendet.

| Einstellung | Bedeutung | Empfehlung |
| --- | --- | --- |
| Abrufintervall | Wie oft die öffentliche Quelle abgefragt wird; 60 bis 3600 Sekunden | 60 Sekunden |
| Einsatz-Entities löschen nach | Aufbewahrung einzelner Einsätze und der Historie | mindestens 7 Tage für eine vollständige Wochenstatistik |
| Kartenposition | Quelle, Stadtmittelpunkt oder automatisch | Automatisch |
| Überwachte Kommunen | Orte, für die Daten und Orts-Entities geführt werden | Nur die Orte wählen, die im Dashboard benötigt werden |

## Zusatz-Entities & Datenumfang

Alle vier Optionen sind standardmäßig eingeschaltet. Sie können unabhängig voneinander abgeschaltet werden, wenn ein schlankeres Setup gewünscht ist.

| Schalter | Wenn aktiviert | Wenn deaktiviert |
| --- | --- | --- |
| Für jeden Einsatz eine eigene Entität anlegen | eine Entity je Einsatz | bestehende dynamische Einsatz-Entities werden entfernt |
| Übersicht für jeden ausgewählten Ort anlegen | eine Zähler- und Listen-Entity je ausgewähltem Ort | Ortsübersichten werden entfernt |
| Letzten Einsatz für jeden ausgewählten Ort anzeigen | eine feste „Letzter Einsatz“-Entity je ausgewähltem Ort | diese Orts-Entities werden entfernt |
| Listen mit Einsatzdetails in den Attributen speichern | Karten können `einsaetze` und `historie` auswerten | Zähler bleiben vorhanden, Listen-Karten zeigen keine Einträge |

## Aufbewahrung

| Auswahl | Wirkung |
| --- | --- |
| 48 Stunden | kompakte Historie, passend zur Datenquelle |
| 7 Tage | vollständige Wochenübersicht ab dem Zeitpunkt der Aktivierung |
| 1 Monat | längere Rückschau |
| Nie | Einsätze bleiben lokal gespeichert, bis die Einstellung geändert wird |

Die Historie wird lokal in Home Assistant geführt. Werden Daten wegen der Aufbewahrungsregel entfernt, aktualisieren sich Historie, Ortsentitäten und „letzter Einsatz je Ort“ automatisch. Es ist keine manuelle Bereinigung nötig.

## Kartenposition

Die öffentliche Quelle liefert derzeit häufig keine Koordinaten. Deshalb gibt es drei Möglichkeiten:

- **Automatisch:** verwendet Quellkoordinaten, wenn vorhanden, sonst den Stadtmittelpunkt.
- **Immer Stadtmittelpunkt:** zeigt eine grobe Ortsposition an.
- **Nur Koordinaten der Quelle:** erzeugt keine Position, solange die Quelle keine Koordinaten bereitstellt.

Ein Stadtmittelpunkt ist keine Einsatzadresse und sollte nur als Orientierung auf einer Karte verstanden werden.
