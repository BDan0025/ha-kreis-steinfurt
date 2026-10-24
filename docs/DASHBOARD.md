# Dashboard-Beispiele

Jede Datei im Ordner [`examples`](../examples/) ist eine einzelne Lovelace-Karte. In Home Assistant: **Dashboard bearbeiten → Karte hinzufügen → Manuell** und den Inhalt der gewünschten YAML-Datei einfügen.

## Übersicht und Status

| Vorlage | Zweck |
| --- | --- |
| [`lovelace_overview.yaml`](../examples/lovelace_overview.yaml) | kompakte Gesamtübersicht |
| [`lovelace_alarm_status.yaml`](../examples/lovelace_alarm_status.yaml) | aktive und abgeschlossene Alarme |
| [`lovelace_statistics.yaml`](../examples/lovelace_statistics.yaml) | heute und letzte 7 Tage |
| [`lovelace_incident_types.yaml`](../examples/lovelace_incident_types.yaml) | Auswertung nach Einsatzarten |

## Letzter Einsatz und Details

| Vorlage | Zweck |
| --- | --- |
| [`lovelace_last_incident_card.yaml`](../examples/lovelace_last_incident_card.yaml) | letzter Einsatz im gesamten Gebiet |
| [`lovelace_incident_detail.yaml`](../examples/lovelace_incident_detail.yaml) | Detailansicht des letzten Einsatzes |
| [`lovelace_latest_incident_map.yaml`](../examples/lovelace_latest_incident_map.yaml) | Kartenansicht, falls eine Position verfügbar ist |

## Orte

Die folgenden Beispiele verwenden Ibbenbüren. Ersetze sowohl Titel als auch Entity-ID durch den gewünschten Ort, etwa `..._rheine` oder `..._emsdetten`.

| Vorlage | Voraussetzung | Zweck |
| --- | --- | --- |
| [`lovelace_ibbenbueren.yaml`](../examples/lovelace_ibbenbueren.yaml) | Ortsübersichten | aktuelle Einsätze eines Ortes |
| [`lovelace_city_overview.yaml`](../examples/lovelace_city_overview.yaml) | Ortsübersichten | aktuell, laufend, heute und letzte 7 Tage |
| [`lovelace_city_last_incident.yaml`](../examples/lovelace_city_last_incident.yaml) | „Letzten Einsatz je Ort“ aktiviert | letzter Einsatz mit Zeit seit Abschluss |
| [`lovelace_city_history.yaml`](../examples/lovelace_city_history.yaml) | Ortsübersichten und Einsatzlisten aktiviert | gespeicherte Historie eines Ortes |

## Listen und Historie

| Vorlage | Zweck |
| --- | --- |
| [`lovelace_active_alarms.yaml`](../examples/lovelace_active_alarms.yaml) | nur laufende Alarme |
| [`lovelace_last_10_incidents.yaml`](../examples/lovelace_last_10_incidents.yaml) | die zehn neuesten Einsätze, einschließlich laufender und abgeschlossener Einsätze |
| [`lovelace_last_10_incidents_map.yaml`](../examples/lovelace_last_10_incidents_map.yaml) | die zehn neuesten Einsätze als geografische Karte |
| [`lovelace_history.yaml`](../examples/lovelace_history.yaml) | Historie im gesamten Gebiet |
| [`lovelace_incident_lists.yaml`](../examples/lovelace_incident_lists.yaml) | kombinierte Listenansichten |
| [`lovelace_cards.yaml`](../examples/lovelace_cards.yaml) | bisheriges Gesamtbeispiel |

> Listen-Karten benötigen den Schalter **Listen mit Einsatzdetails in den Attributen speichern**. Die Listen sind zum Schutz der Datenbank auf 50 Einträge, die Orts-Historie auf 25 Einträge begrenzt.

## Screenshots ergänzen

Lege die Bilder in [`docs/images`](images/) ab und verlinke sie in dieser Datei, zum Beispiel:

```markdown
![Ortsübersicht Ibbenbüren](images/ortsuebersicht-ibbenbueren.png)
```

Empfohlene Dateinamen stehen im [Bilderbereich](images/README.md).
