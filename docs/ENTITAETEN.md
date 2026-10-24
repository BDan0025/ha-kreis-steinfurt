# Entitäten

## Übersichten für das gesamte ausgewählte Gebiet

| Entität | Zustand | Wichtige Attribute |
| --- | --- | --- |
| `sensor.kreis_steinfurt_einsaetze` | Anzahl veröffentlichter Einsätze | `laufende_einsaetze`, `einsatznummern`, `orte`, optional `einsaetze` |
| `sensor.kreis_steinfurt_laufende_einsatze` | Anzahl laufender Einsätze | optional `einsaetze` |
| `sensor.kreis_steinfurt_einsatze_letzte_24_stunden` | Anzahl der letzten 24 Stunden | optional `einsaetze` |
| `sensor.kreis_steinfurt_einsatzhistorie` | Anzahl lokal gespeicherter Einsätze | `aufbewahrung`, `einsatzarten`, optional `einsaetze` |
| `sensor.kreis_steinfurt_einsatze_heute` | Anzahl seit Tagesbeginn | `gesamt`, `nach_ort`, `nach_einsatzart` |
| `sensor.kreis_steinfurt_einsatze_letzte_7_tage` | Anzahl der letzten sieben Tage | `gesamt`, `nach_ort`, `nach_einsatzart` |
| `sensor.kreis_steinfurt_einsatzarten` | Anzahl erkannter Einsatzarten | `einsatzarten` |
| `sensor.kreis_steinfurt_abrufintervall` | Abrufintervall in Sekunden | – |

## Letzter Einsatz im gesamten Gebiet

`sensor.kreis_steinfurt_letzter_einsatz` hat als Zustand den Einsatzstatus, zum Beispiel `abgeschlossen`. Die Attribute enthalten die vollständigen Daten zum neuesten Einsatz: `einsatznummer`, `einsatzart`, `ort`, `beginn`, `beginn_iso`, `status`, `strasse`, `sachverhalt`, `abgeschlossen_am`, `abgeschlossen_vor`, `dauer`, `dauer_sekunden`, `latitude`, `longitude` und `kartenposition`.

`dauer` bedeutet bei einem abgeschlossenen Einsatz die Zeit von Beginn bis Abschluss. Bei einem laufenden Einsatz ist es die Laufzeit bis jetzt. `abgeschlossen_vor` wird im Zehn-Minuten-Takt aktualisiert, ohne einen neuen Abruf der Quelle auszulösen.

## Ortsübersichten

Für jeden ausgewählten Ort entsteht eine feste Entität. Beispiele:

| Entität | Zustand | Attribute |
| --- | --- | --- |
| `sensor.kreis_steinfurt_einsatze_ibbenburen` | aktuell veröffentlichte Einsätze in Ibbenbüren | `laufende_einsaetze`, `einsatzanzahl_heute`, `einsatzanzahl_letzte_7_tage`, optional `einsaetze`, `historie` |
| `sensor.kreis_steinfurt_einsatze_rheine` | aktuell veröffentlichte Einsätze in Rheine | wie oben |

## Letzter Einsatz je Ort

Für jeden ausgewählten Ort entsteht zusätzlich eine eigene Entität:

```text
sensor.kreis_steinfurt_letzter_einsatz_<ort>
```

Beispiel: `sensor.kreis_steinfurt_letzter_einsatz_ibbenburen`.

Der Zustand ist `HH:MM`:

- bei abgeschlossenen Einsätzen: Zeit seit Abschluss, zum Beispiel `02:10`;
- bei laufenden Einsätzen: bisherige Laufzeit;
- ohne gespeicherten Einsatz: `unbekannt`.

Die Attribute entsprechen dem letzten Einsatz und enthalten zusätzlich `zeitangabe` mit `seit Abschluss` oder `Laufzeit`.

## Einzelne Einsatz-Entities

Optional erhält jeder Einsatz eine eigene Entity:

```text
sensor.kreis_steinfurt_einsatz_<einsatznummer>
```

Beispiel: `sensor.kreis_steinfurt_einsatz_26069895`. Sie bleibt bis zum Ablauf der eingestellten Aufbewahrung bestehen. Nach dem Entfernen aus der öffentlichen Liste bleiben der letzte bekannte Status und die Details also noch verfügbar, bis die Aufbewahrung endet.

> Die Entity-IDs verwenden die Home-Assistant-Schreibweise ohne Umlaute, etwa `ibbenburen` statt `Ibbenbüren`.
