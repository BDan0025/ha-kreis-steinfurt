# HACS-Veröffentlichung

Die Dateien im Repository sind für HACS vorbereitet. Vor der offiziellen Aufnahme sind noch diese Schritte direkt auf GitHub erforderlich:

1. Das Repository öffentlich schalten.
2. Eine kurze Beschreibung und die Themen `home-assistant`, `hacs`, `custom-component`, `germany` und `kreis-steinfurt` eintragen.
3. GitHub Issues aktivieren.
4. Version 1.0.0 pushen und abwarten, bis die Workflows **HACS-Validierung** und **Hassfest** erfolgreich sind.
5. Eine GitHub-Release mit dem Tag `v1.0.0` erstellen.
6. Im Repository `hacs/default` einen Pull Request erstellen und die Integration alphabetisch in `integration` eintragen.

Bis zur Aufnahme in die offizielle HACS-Liste kann das Repository bereits als **benutzerdefiniertes Repository** in HACS installiert werden.

## KI-Unterstützung

Die HACS-Vorbereitung wurde mit KI-Unterstützung erstellt. Das umfasst diese Checkliste, die GitHub-Workflows, Issue-Vorlagen und das Marken-Icon. Die Integrationsfunktionen wurden vor der Veröffentlichung in Home Assistant getestet.

## Wichtige Hinweise

- Das Icon liegt unter `brand/icon.png`.
- Die HACS-Prüfung meldet auch fehlende GitHub-Einstellungen wie Beschreibung, Themen oder deaktivierte Issues. Diese Einstellungen lassen sich erst nach dem Push direkt auf GitHub setzen.
- Nach der Veröffentlichung bleibt die Versionsnummer in `manifest.json`, `pyproject.toml`, README und Änderungsübersicht bei jedem Release gleich zu pflegen.
