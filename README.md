# ha-kreis-steinfurt
Home Assistant integration for Kreis Steinfurt emergency incidents

https://github.com/BDan0025/ha-kreis-steinfurt




Aufbau

ha-kreis-steinfurt/
│
├── custom_components/
│   └── kreis_steinfurt/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── coordinator.py
│       ├── client.py          ← HTTP-Zugriff
│       ├── parser.py          ← HTML → Modelle
│       ├── models.py          ← Dataclasses
│       ├── sensor.py
│       ├── entity.py
│       ├── const.py
│       ├── diagnostics.py
│       ├── strings.json
│       ├── translations/
│       │   ├── de.json
│       │   └── en.json
│       └── icons.json
│
├── tests/
│   ├── sample_page.html
│   ├── test_parser.py
│   └── test_client.py
│
├── hacs.json
├── README.md
├── LICENSE
├── pyproject.toml
└── requirements_dev.txt