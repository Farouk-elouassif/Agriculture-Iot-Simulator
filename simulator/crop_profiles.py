from typing import Dict


# Baseline target values by crop for lightweight realism.
CROP_PROFILES: Dict[str, Dict[str, float]] = {
    "tomato": {
        "ph": 6.4,
        "moisture": 68.0,
        "temperature": 24.0,
        "ec": 1.4,
        "nitrogen": 50.0,
        "phosphorus": 35.0,
        "potassium": 55.0,
        "organic_matter": 3.1,
        "salinity": 0.8,
    },
    "orange": {
        "ph": 6.2,
        "moisture": 62.0,
        "temperature": 22.0,
        "ec": 1.1,
        "nitrogen": 42.0,
        "phosphorus": 28.0,
        "potassium": 48.0,
        "organic_matter": 2.8,
        "salinity": 0.7,
    },
    "apple": {
        "ph": 6.5,
        "moisture": 58.0,
        "temperature": 19.0,
        "ec": 1.0,
        "nitrogen": 38.0,
        "phosphorus": 25.0,
        "potassium": 44.0,
        "organic_matter": 2.6,
        "salinity": 0.6,
    },
}


def get_crop_profile(crop: str) -> Dict[str, float]:
    return CROP_PROFILES.get(crop.lower(), CROP_PROFILES["tomato"]).copy()
