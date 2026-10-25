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
| `sensor.kreis_steinfurt_quellseiten` | Anzahl aktuell gefundener Seiten der Kreis-Liste | `einsaetze_auf_der_quelle`, `abgerufene_einsaetze` |
| `sensor.kreis_steinfurt_einsaetze_auf_der_quelle` | Gesamtzahl laut Kreis-Seite | `quellseiten`, `abgerufene_einsaetze` |
| `sensor.kreis_steinfurt_letzte_aktualisierung` | letzter erfolgreicher vollständiger Abruf | – |

## Letzter Einsatz im gesamten Gebiet

`sensor.kreis_steinfurt_letzter_einsatz` hat als Zustand den Einsatzstatus, zum Beispiel `abgeschlossen`. Die Attribute enthalten die vollständigen Daten zum neuesten Einsatz: `einsatznummer`, `einsatzart`, `ort`, `beginn`, `beginn_iso`, `status`, `strasse`, `sachverhalt`, `latitude`, `longitude` und `kartenposition`.

Die öffentliche Quelle liefert keine belastbare Abschlusszeit. Deshalb erzeugt die Integration keine Abschlusszeit, keine Einsatzdauer und keine „Zeit seit Abschluss“. `beginn` wird unverändert aus der Quelle übernommen.

## Kartenpunkte der letzten zehn Einsätze

Die zehn festen Entitäten `sensor.kreis_steinfurt_kartenpunkt_1` bis `sensor.kreis_steinfurt_kartenpunkt_10` bilden immer die zehn neuesten gespeicherten Einsätze ab. Sie sind für die Lovelace-Kartenansicht gedacht und werden bei neuen Einsätzen automatisch neu belegt.

Jeder Kartenpunkt enthält die gleichen Details wie ein einzelner Einsatz, insbesondere `position`, `ort`, `einsatzart`, `beginn`, `status`, `latitude`, `longitude` und `kartenposition`. Sein Anzeigename und die Kartenmarkierung zeigen die Position 1 bis 10, passend zur „Letzte 10 Einsätze“-Tabelle. Ohne hinterlegte Position bleibt der betreffende Punkt in der Karte unsichtbar.

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

Der Zustand ist der zuletzt von der Quelle gemeldete Einsatzstatus:

- zum Beispiel `laufend` oder `abgeschlossen`;
- ohne gespeicherten Einsatz: `unbekannt`.

Die Attribute entsprechen dem letzten Einsatz. Zeitwerte werden nur dargestellt, wenn die Quelle sie liefert.

## Einzelne Einsatz-Entities

Optional erhält jeder Einsatz eine eigene Entity:

```text
sensor.kreis_steinfurt_einsatz_<einsatznummer>
```

Beispiel: `sensor.kreis_steinfurt_einsatz_26069895`. Sie bleibt bis zum Ablauf der eingestellten Aufbewahrung bestehen. Nach dem Entfernen aus der öffentlichen Liste bleiben der letzte bekannte Status und die Details also noch verfügbar, bis die Aufbewahrung endet.

> Die Entity-IDs verwenden die Home-Assistant-Schreibweise ohne Umlaute, etwa `ibbenburen` statt `Ibbenbüren`.
