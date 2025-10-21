FISH_PROFILES = {
    "carp": {
        "temp_range": (18, 28),
        "ideal_cloud": 40,
        "prefers_low_pressure": True
    },
    "trout": {
        "temp_range": (10, 18),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "pike": {
        "temp_range": (10, 20),
        "ideal_cloud": 50,
        "prefers_low_pressure": True
    },
    "largemouth_bass": {
        "temp_range": (18, 27),
        "ideal_cloud": 50,
        "prefers_low_pressure": False
    },
    "smallmouth_bass": {
        "temp_range": (16, 24),
        "ideal_cloud": 50,
        "prefers_low_pressure": False
    },
    "walleye": {
        "temp_range": (12, 22),
        "ideal_cloud": 60,
        "prefers_low_pressure": True
    },
    "catfish": {
        "temp_range": (20, 30),
        "ideal_cloud": 40,
        "prefers_low_pressure": True
    },
    "bluegill": {
        "temp_range": (20, 28),
        "ideal_cloud": 50,
        "prefers_low_pressure": False
    },
    "crappie": {
        "temp_range": (15, 25),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "perch": {
        "temp_range": (15, 22),
        "ideal_cloud": 50,
        "prefers_low_pressure": False
    },
    "muskellunge": {
        "temp_range": (15, 25),
        "ideal_cloud": 50,
        "prefers_low_pressure": True
    },
    "brook_trout": {
        "temp_range": (10, 18),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "brown_trout": {
        "temp_range": (12, 20),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "rainbow_trout": {
        "temp_range": (10, 18),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "zander": {
        "temp_range": (12, 22),
        "ideal_cloud": 80,
        "prefers_low_pressure": True
    },
    "bream": { # Assuming this refers to common bream (Brachse)
        "temp_range": (18, 25),
        "ideal_cloud": 70,
        "prefers_low_pressure": True
    },
    "roach": { # Assuming this refers to Rotauge
        "temp_range": (15, 22),
        "ideal_cloud": 60,
        "prefers_low_pressure": True
    },
    "grayling": { # Äsche
        "temp_range": (8, 16),
        "ideal_cloud": 70,
        "prefers_low_pressure": False
    },
    "salmon_atlantic": {
        "temp_range": (8, 15),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "salmon_chinook": {
        "temp_range": (8, 15),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "steelhead": {
        "temp_range": (8, 16),
        "ideal_cloud": 60,
        "prefers_low_pressure": False
    },
    "common_nase": { # Nase
        "temp_range": (14, 20),
        "ideal_cloud": 70,
        "prefers_low_pressure": True # Generally found in flowing water, pressure might be less of a direct factor
    },
    "chub": { # Döbel
        "temp_range": (15, 24),
        "ideal_cloud": 60,
        "prefers_low_pressure": True
    },
    "char": { # Saibling (likely Alpine Char or similar)
        "temp_range": (8, 14),
        "ideal_cloud": 70,
        "prefers_low_pressure": False
    },
    "huchen": { # Huchen (Danube Salmon)
        "temp_range": (5, 15),
        "ideal_cloud": 60,
        "prefers_low_pressure": False # Prefers cold, clear, flowing water
    },
    "bullhead": { # Mühlkoppe
        "temp_range": (8, 18),
        "ideal_cloud": 80,
        "prefers_low_pressure": True # Often found on the bottom, might be less sensitive to pressure
    },
    "whitefish": { # Renke (various species)
        "temp_range": (8, 16),
        "ideal_cloud": 70,
        "prefers_low_pressure": False
    },
    "burbot": { # Rutte
        "temp_range": (2, 10), # Prefers very cold water
        "ideal_cloud": 80,
        "prefers_low_pressure": True # Often active at night or in low light
    },
    "asp": { # Schied
        "temp_range": (16, 26),
        "ideal_cloud": 50,
        "prefers_low_pressure": True
    },
    "tench": { # Schleie
        "temp_range": (18, 25),
        "ideal_cloud": 80,
        "prefers_low_pressure": True # Often found in weedy areas with lower light
    },
    "rudd": { # Rotfeder
        "temp_range": (16, 24),
        "ideal_cloud": 60,
        "prefers_low_pressure": True
    },
    "bleak": { # Laube
        "temp_range": (14, 22),
        "ideal_cloud": 60,
        "prefers_low_pressure": True # Often found in schools near the surface
    },
    "wels_catfish": { # Wels (European Catfish)
        "temp_range": (20, 30),
        "ideal_cloud": 70,
        "prefers_low_pressure": True # Often more active during low light conditions
    }
}

def get_fish_species() -> list[str]:
    return list(FISH_PROFILES.keys())