# Kreis Steinfurt Einsätze

Home-Assistant-Integration für die öffentlich veröffentlichte Liste der [aktuellen Einsätze des Kreises Steinfurt](https://www.kreis-steinfurt.de/kv_steinfurt/Kreisverwaltung/%C3%84mter/Amt%20f%C3%BCr%20Bev%C3%B6lkerungsschutz/Kreisleitstelle/Aktuelle%20Eins%C3%A4tze/).

> **Aktuelle Version: 0.6.0** · Die Daten stammen ausschließlich aus der öffentlichen Quelle und können unvollständig, verspätet oder fehlerhaft sein.

## Das bietet die Integration

| Bereich | Funktion |
| --- | --- |
| Übersicht | Einsätze, laufende Alarme, heute, letzte 24 Stunden und letzte 7 Tage |
| Orte | frei auswählbare Kommunen mit eigener Ortsübersicht |
| Letzter Einsatz | eine feste Entität je ausgewähltem Ort, inklusive Zeit seit Abschluss |
| Historie | lokale Speicherung für 48 Stunden, 7 Tage, 1 Monat oder dauerhaft |
| Dashboard | einzeln nutzbare Lovelace-Karten für Übersicht, Orte, Historie und Details |
| Datenumfang | begrenzte Listenattribute und abschaltbare Zusatz-Entities |

## Schnellstart

1. Den Ordner `custom_components/kreis_steinfurt` nach `<Home-Assistant-Konfiguration>/custom_components/kreis_steinfurt` kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Kreis Steinfurt Einsätze** suchen und einrichten.
4. Unter **Konfigurieren** die gewünschten Orte auswählen.
5. Eine Karte aus [`examples`](examples/) als **Manuelle Karte** in ein Dashboard einfügen.

## Dokumentation

| Thema | Inhalt |
| --- | --- |
| [Entitäten](docs/ENTITAETEN.md) | Alle Übersicht-, Orts- und Einsatz-Entities mit Attributen |
| [Einstellungen](docs/EINSTELLUNGEN.md) | Abrufintervall, Aufbewahrung, Orte, Kartenposition und Schalter |
| [Dashboard-Beispiele](docs/DASHBOARD.md) | Jede Lovelace-Karte einzeln erklärt |
| [Bilder & Screenshots](docs/images/README.md) | Bereich für Screenshots der Dashboard-Beispiele |
| [Änderungen](docs/CHANGELOG.md) | Funktionsstände und Versionsverlauf |

## Wichtige Entitäten

| Entität | Bedeutung |
| --- | --- |
| `sensor.kreis_steinfurt_einsaetze` | Alle aktuell von der Quelle veröffentlichten Einsätze |
| `sensor.kreis_steinfurt_laufende_einsatze` | Einsätze, deren Status nicht `abgeschlossen` ist |
| `sensor.kreis_steinfurt_letzter_einsatz` | Details zum neuesten Einsatz im gesamten ausgewählten Gebiet |
| `sensor.kreis_steinfurt_einsatzhistorie` | Anzahl der lokal gespeicherten Einsätze |
| `sensor.kreis_steinfurt_einsatze_heute` | Einsätze seit Tagesbeginn |
| `sensor.kreis_steinfurt_einsatze_letzte_7_tage` | Einsätze der vergangenen sieben Tage |
| `sensor.kreis_steinfurt_abrufintervall` | Eingestelltes Abrufintervall in Sekunden |
| `sensor.kreis_steinfurt_einsatze_ibbenburen` | Ortsübersicht, hier als Beispiel Ibbenbüren |
| `sensor.kreis_steinfurt_letzter_einsatz_ibbenburen` | Letzter gespeicherter Einsatz in Ibbenbüren |

Die Orts-Entitäten entstehen für **jeden ausgewählten Ort**, selbst wenn dort noch kein Einsatz gespeichert ist. Für andere Orte wird der Ortsname in der Entity-ID entsprechend ersetzt, zum Beispiel `..._emsdetten` oder `..._rheine`.

## Dashboard-Beispiele

Alle Vorlagen liegen im Ordner [`examples`](examples/) und sind unabhängig voneinander nutzbar. Besonders hilfreich für den Einstieg sind:

- [Kompakte Übersicht](examples/lovelace_overview.yaml)
- [Letzter Einsatz einer Stadt](examples/lovelace_city_last_incident.yaml)
- [Ortsübersicht](examples/lovelace_city_overview.yaml)
- [Aktive Alarme](examples/lovelace_active_alarms.yaml)
- [Letzte 10 Einsätze](examples/lovelace_last_10_incidents.yaml)
- [Letzte 10 Einsätze – Karte](examples/lovelace_last_10_incidents_map.yaml)
- [Einsatzhistorie](examples/lovelace_history.yaml)

Die vollständige Liste samt Voraussetzungen und Anpassung auf einen anderen Ort steht in der [Dashboard-Dokumentation](docs/DASHBOARD.md).

## Hinweise zur Datenquelle

Die Quelle veröffentlicht Einsätze der letzten rund 48 Stunden. Straße, Sachverhalt und genaue Koordinaten sind nicht immer verfügbar. Als optionale Kartenposition kann deshalb ein Stadtmittelpunkt verwendet werden; das ist nur eine grobe Ortsangabe, niemals eine Einsatzadresse.

Die Detail- und Listenattribute sind bewusst begrenzt, damit die Home-Assistant-Datenbank klein bleibt. Mehr dazu steht bei den [Einstellungen](docs/EINSTELLUNGEN.md).

## Entwicklung

```shell
python -m pip install -r requirements_dev.txt
python -m pytest
```
