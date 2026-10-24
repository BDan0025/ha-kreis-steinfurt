"""Constants for Kreis Steinfurt integration."""

DOMAIN = "kreis_steinfurt"

NAME = "Kreis Steinfurt Einsätze"

CONF_AREAS = "areas"
CONF_INCIDENT_TYPES = "incident_types"
CONF_RETENTION = "retention"
CONF_SCAN_INTERVAL = "scan_interval"

RETENTION_48_HOURS = "48_hours"
RETENTION_7_DAYS = "7_days"
RETENTION_30_DAYS = "30_days"
RETENTION_NEVER = "never"

RETENTION_OPTIONS = (
    RETENTION_48_HOURS,
    RETENTION_7_DAYS,
    RETENTION_30_DAYS,
    RETENTION_NEVER,
)

KREIS_STEINFURT_AREAS = (
    "Altenberge",
    "Emsdetten",
    "Greven",
    "Hörstel",
    "Hopsten",
    "Horstmar",
    "Ibbenbüren",
    "Ladbergen",
    "Laer",
    "Lengerich",
    "Lienen",
    "Lotte",
    "Metelen",
    "Mettingen",
    "Neuenkirchen",
    "Nordwalde",
    "Ochtrup",
    "Recke",
    "Rheine",
    "Saerbeck",
    "Steinfurt",
    "Tecklenburg",
    "Westerkappeln",
    "Wettringen",
)

DEFAULT_SCAN_INTERVAL = 60
MIN_SCAN_INTERVAL = 60
MAX_SCAN_INTERVAL = 3600

SOURCE_URL = (
    "https://www.kreis-steinfurt.de/"
    "kv_steinfurt/Kreisverwaltung/"
    "%C3%84mter/Amt%20f%C3%BCr%20Bev%C3%B6lkerungsschutz/"
    "Kreisleitstelle/Aktuelle%20Eins%C3%A4tze/"
)
