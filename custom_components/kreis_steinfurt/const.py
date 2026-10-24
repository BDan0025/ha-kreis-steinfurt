"""Constants for Kreis Steinfurt integration."""

DOMAIN = "kreis_steinfurt"

NAME = "Kreis Steinfurt Einsätze"

CONF_AREAS = "areas"
CONF_INCIDENT_TYPES = "incident_types"
CONF_KARTENPOSITION = "kartenposition"
CONF_RETENTION = "retention"
CONF_SCAN_INTERVAL = "scan_interval"

RETENTION_48_HOURS = "48_hours"
RETENTION_7_DAYS = "7_days"
RETENTION_30_DAYS = "30_days"
RETENTION_NEVER = "never"

MAP_LOCATION_AUTOMATIC = "automatic"
MAP_LOCATION_CITY = "city"
MAP_LOCATION_SOURCE = "source"
MAP_LOCATION_OPTIONS = (
    MAP_LOCATION_AUTOMATIC,
    MAP_LOCATION_CITY,
    MAP_LOCATION_SOURCE,
)

# Stadtmittelpunkte für eine grobe Einsatzdarstellung, nicht als Einsatzadresse.
CITY_COORDINATES = {
    "Altenberge": (52.050, 7.470), "Emsdetten": (52.173, 7.533),
    "Greven": (52.093, 7.610), "Hörstel": (52.297, 7.590),
    "Hopsten": (52.383, 7.600), "Horstmar": (52.082, 7.306),
    "Ibbenbüren": (52.279, 7.714), "Ladbergen": (52.137, 7.742),
    "Laer": (52.056, 7.357), "Lengerich": (52.186, 7.860),
    "Lienen": (52.147, 7.984), "Lotte": (52.282, 7.917),
    "Metelen": (52.144, 7.469), "Mettingen": (52.317, 7.783),
    "Neuenkirchen": (52.244, 7.371), "Nordwalde": (52.084, 7.481),
    "Ochtrup": (52.209, 7.316), "Recke": (52.361, 7.721),
    "Rheine": (52.285, 7.440), "Saerbeck": (52.174, 7.633),
    "Steinfurt": (52.150, 7.337), "Tecklenburg": (52.219, 7.813),
    "Westerkappeln": (52.323, 7.883), "Wettringen": (52.209, 7.318),
}

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
