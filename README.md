# Kreis Steinfurt Einsätze für Home Assistant

Diese Custom Integration liest die öffentlich verfügbare Liste der
[aktuellen Einsätze](https://www.kreis-steinfurt.de/kv_steinfurt/Kreisverwaltung/%C3%84mter/Amt%20f%C3%BCr%20Bev%C3%B6lkerungsschutz/Kreisleitstelle/Aktuelle%20Eins%C3%A4tze/)
der Feuerwehren im Kreis Steinfurt aus.

Die Quelle enthält Einsätze der letzten 48 Stunden. Sie wird standardmäßig alle
60 Sekunden aktualisiert.

## Installation

1. Den Ordner `custom_components/kreis_steinfurt` nach
   `<Home-Assistant-Konfiguration>/custom_components/kreis_steinfurt` kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach
   **Kreis Steinfurt Einsätze** suchen und einrichten.

## Sensor

Die Integration erstellt diese Übersichten:

- `sensor.kreis_steinfurt_einsaetze` – Anzahl aller veröffentlichten Einsätze
  der letzten 48 Stunden
- `sensor.kreis_steinfurt_laufende_einsaetze` – Anzahl der Einträge, die nicht
  als `abgeschlossen` markiert sind
- `sensor.kreis_steinfurt_einsaetze_letzte_24_stunden` – Anzahl seit den
  vergangenen 24 Stunden
- `sensor.kreis_steinfurt_einsatzhistorie` – Anzahl der gespeicherten Einsätze
  innerhalb der gewählten Aufbewahrungsdauer
- `sensor.kreis_steinfurt_einsaetze_heute` – Gesamtzahl seit Tagesbeginn
- `sensor.kreis_steinfurt_einsaetze_letzte_7_tage` – Gesamtzahl der letzten
  sieben Tage
- `sensor.kreis_steinfurt_einsatzarten` – bekannte Einsatzarten mit Zählern in
  den Attributen
- `sensor.kreis_steinfurt_letzter_einsatz` – vollständige Details des jeweils
  zuletzt veröffentlichten Einsatzes

Zusätzlich entstehen dynamisch Sensoren für jeden Einsatz sowie jede in der
Liste vorkommende Stadt. Ein Einsatzsensor hat den Status als Zustand und die
Attribute `einsatznummer`, `einsatzart`, `ort`, `beginn`, `status`, `strasse`,
  `sachverhalt`, `latitude`, `longitude` und `kartenposition`. Straße und
Sachverhalt sind `null`, solange die öffentliche Quelle diese Angaben nicht
veröffentlicht. Koordinaten können wahlweise als Stadtmittelpunkt ergänzt werden.
Zusätzlich sind `erstmals_gesehen`, `letzte_aenderung`, `abgeschlossen_am`,
`abgeschlossen_vor`, `dauer_sekunden` und `dauer` vorhanden. `dauer` ist bei
laufenden Einsätzen die Laufzeit bis jetzt, bei abgeschlossenen Einsätzen die
Zeit zwischen Beginn und Abschluss. `abgeschlossen_vor` wird nur für
abgeschlossene Einsätze ausgegeben und aktualisiert sich im 10-Minuten-Takt,
ohne einen weiteren Abruf der Quelle auszulösen. Die dynamische Entity wird
nach Ablauf der ausgewählten Aufbewahrung entfernt; die Einsatzhistorie enthält den
kompletten Verlauf bis zu diesem Zeitpunkt. Bis zur Löschung behält sie ihren
letzten bekannten Zustand und wechselt nicht zwischen Status und
„Nicht verfügbar“.

## Dashboard-Beispiele

Jede Vorlage kann einzeln als **Manuelle Karte** in ein Home-Assistant-Dashboard
eingefügt werden. Die Beispiele verwenden die Entity-IDs dieser Integration:

- [`lovelace_overview.yaml`](examples/lovelace_overview.yaml) – kompakte Übersicht
- [`lovelace_ibbenbueren.yaml`](examples/lovelace_ibbenbueren.yaml) – aktuelle Einsätze in Ibbenbüren
- [`lovelace_city_overview.yaml`](examples/lovelace_city_overview.yaml) – Stadtübersicht mit aktuell, laufend, heute und letzte 7 Tage
- [`lovelace_city_last_incident.yaml`](examples/lovelace_city_last_incident.yaml) – letzter Einsatz einer Stadt mit Dauer
- [`lovelace_city_history.yaml`](examples/lovelace_city_history.yaml) – gespeicherte Einsatzhistorie einer Stadt
- [`lovelace_last_incident_card.yaml`](examples/lovelace_last_incident_card.yaml) – letzter Einsatz mit Dauer
- [`lovelace_incident_detail.yaml`](examples/lovelace_incident_detail.yaml) – automatisch wechselnde Details des letzten Einsatzes
- [`lovelace_latest_incident_map.yaml`](examples/lovelace_latest_incident_map.yaml) – Karte des letzten Einsatzes
- [`lovelace_alarm_status.yaml`](examples/lovelace_alarm_status.yaml) – aktive und abgeschlossene Alarme
- [`lovelace_statistics.yaml`](examples/lovelace_statistics.yaml) – heute und letzte 7 Tage
- [`lovelace_incident_types.yaml`](examples/lovelace_incident_types.yaml) – Auswertung nach Einsatzarten
- [`lovelace_active_alarms.yaml`](examples/lovelace_active_alarms.yaml) – Liste aktiver Alarme
- [`lovelace_history.yaml`](examples/lovelace_history.yaml) – Einsatzhistorie

Für eine andere Stadt in den Ortskarten Titel und Entity-IDs entsprechend
anpassen. Als Vorlage dient Ibbenbüren, zum Beispiel
`sensor.kreis_steinfurt_einsatze_ibbenburen`.

Die bisherigen kombinierten Vorlagen
[`lovelace_cards.yaml`](examples/lovelace_cards.yaml) und
[`lovelace_incident_lists.yaml`](examples/lovelace_incident_lists.yaml) bleiben
als Gesamtbeispiele erhalten. Die Listen-Attribute sind zum Schutz der
Home-Assistant-Datenbank auf die 50 neuesten Einträge begrenzt.
Die zusätzliche Historie eines Ortssensors ist auf 25 Einträge begrenzt.

Die Angaben stammen ausschließlich von der veröffentlichten Liste des Kreises
Steinfurt und können sich jederzeit ändern.

## Einstellungen

Unter **Einstellungen → Geräte & Dienste → Kreis Steinfurt Einsätze →
Konfigurieren** lassen sich das Abrufintervall (60 bis 3600 Sekunden) sowie die
überwachten Kommunen per Mehrfachauswahl festlegen.
Die Übersichtssensoren sowie Einsatz- und Ortssensoren berücksichtigen nur diese
Auswahl.

`sensor.kreis_steinfurt_abrufintervall` zeigt den aktuell verwendeten Wert in
Sekunden an.

Für die Kartenposition einzelner Einsatz-Entities kann gewählt werden, ob nur
Koordinaten der Quelle verwendet werden, immer der Stadtmittelpunkt angezeigt
wird oder automatisch auf den Stadtmittelpunkt zurückgefallen wird. Da die
Quelle aktuell keine Koordinaten veröffentlicht, liefert „automatisch“ derzeit
den Stadtmittelpunkt; „nur Quelle“ erzeugt aktuell keine Position. Die
Stadtmittelpunkte dienen ausschließlich zur groben Ortsdarstellung.

Die Einsatzarten werden aus den veröffentlichten Daten automatisch erkannt und
über `sensor.kreis_steinfurt_einsatzarten` mitsamt ihren Zählern bereitgestellt.

Für einzelne Einsatz-Entities kann eine Aufbewahrung von 48 Stunden, 7 Tagen,
einem Monat oder dauerhaft gewählt werden. Die Integration speichert dafür die
zuletzt veröffentlichten Einsatzdetails lokal in Home Assistant und entfernt die
Entity nach Ablauf der gewählten Zeit.

Die Sensoren „heute“ und „letzte 7 Tage“ verwenden diese gespeicherte Historie.
Für eine vollständige 7-Tage-Statistik muss die Aufbewahrung deshalb mindestens
auf 7 Tage, 1 Monat oder „Nie“ eingestellt sein.

## Entwicklung

```shell
python -m pip install -r requirements_dev.txt
python -m pytest
```
