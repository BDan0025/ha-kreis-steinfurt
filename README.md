# Kreis Steinfurt Einsätze

[![HACS-Validierung](https://github.com/BDan0025/ha-kreis-steinfurt/actions/workflows/validate.yaml/badge.svg)](https://github.com/BDan0025/ha-kreis-steinfurt/actions/workflows/validate.yaml)
[![Hassfest](https://github.com/BDan0025/ha-kreis-steinfurt/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/BDan0025/ha-kreis-steinfurt/actions/workflows/hassfest.yaml)

Home-Assistant-Integration für die öffentlich veröffentlichte Liste der [aktuellen Einsätze des Kreises Steinfurt](https://www.kreis-steinfurt.de/kv_steinfurt/Kreisverwaltung/%C3%84mter/Amt%20f%C3%BCr%20Bev%C3%B6lkerungsschutz/Kreisleitstelle/Aktuelle%20Eins%C3%A4tze/).

> **Aktuelle Version: 1.0.0** · Die Daten stammen ausschließlich aus der öffentlichen Quelle und können unvollständig, verspätet oder fehlerhaft sein.

## Das bietet die Integration

| Bereich | Funktion |
| --- | --- |
| Übersicht | Einsätze, laufende Alarme, heute, letzte 24 Stunden und letzte 7 Tage |
| Orte | frei auswählbare Kommunen mit eigener Ortsübersicht |
| Letzter Einsatz | eine feste Entität je ausgewähltem Ort mit dem zuletzt von der Quelle gemeldeten Status |
| Abschluss-Erkennung | Zeitpunkt und Einsatzzeit bis zur ersten erkannten Meldung `abgeschlossen` |
| Historie | lokale Speicherung für 48 Stunden, 7 Tage, 1 Monat oder dauerhaft |
| Dashboard | einzeln nutzbare Lovelace-Karten für Übersicht, Orte, Historie und Details |
| Datenumfang | begrenzte Listenattribute und abschaltbare Zusatz-Entities |

## Installation

### Über HACS als eigenes Repository

1. In HACS **Integrationen** öffnen und oben rechts **Benutzerdefinierte Repositorys** wählen.
2. `https://github.com/BDan0025/ha-kreis-steinfurt` einfügen und als Kategorie **Integration** wählen.
3. Die Integration installieren und Home Assistant neu starten.
4. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Kreis Steinfurt Einsätze** suchen.

### Manuelle Installation

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
| [HACS-Veröffentlichung](docs/HACS.md) | Checkliste für GitHub-Release und offizielle HACS-Aufnahme |
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
| `sensor.kreis_steinfurt_quellseiten` | Anzahl der aktuell auf der Kreis-Seite gefundenen Seiten |
| `sensor.kreis_steinfurt_einsatze_auf_der_quelle` | Gesamtzahl der aktuell auf der Kreis-Seite veröffentlichten Einsätze |
| `sensor.kreis_steinfurt_letzte_aktualisierung` | Zeitpunkt des letzten erfolgreichen vollständigen Abrufs |
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

## Unterstützung und Fehler melden

- Fehler oder fehlende Orte bitte als [GitHub-Issue](https://github.com/BDan0025/ha-kreis-steinfurt/issues/new/choose) melden.
- Bitte immer die Integrationsversion, die Home-Assistant-Version und den passenden Protokolleintrag angeben.
- Die Integration ist unabhängig vom Kreis Steinfurt und verarbeitet ausschließlich dessen öffentlich bereitgestellte Einsatzliste.

## KI-Unterstützung

Die HACS-Vorbereitung dieses Projekts – Dokumentation, Prüf-Workflows, Issue-Vorlagen und Marken-Icon – wurde mit Unterstützung von KI erstellt. Die Funktionen wurden anschließend in Home Assistant praktisch geprüft.

## Entwicklung

```shell
python -m pip install -r requirements_dev.txt
python -m pytest
```
