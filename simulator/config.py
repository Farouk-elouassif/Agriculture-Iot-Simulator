from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from simulator.models import AreaConfig, Config, FarmConfig, SimulationConfig


def _parse_areas(raw_areas: List[Dict[str, Any]]) -> List[AreaConfig]:
    areas: List[AreaConfig] = []
    for area in raw_areas:
        areas.append(
            AreaConfig(
                id=str(area["id"]),
                crop=str(area["crop"]).lower(),
                devices=[str(device_id) for device_id in area.get("devices", [])],
            )
        )
    return areas


def load_config(config_path: str) -> Config:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with path.open("r", encoding="utf-8") as file_handle:
        raw = yaml.safe_load(file_handle) or {}

    simulation_raw = raw.get("simulation", {})
    simulation = SimulationConfig(
        event_interval_seconds=int(simulation_raw.get("event_interval_seconds", 5)),
        weather_refresh_minutes=int(simulation_raw.get("weather_refresh_minutes", 15)),
        seed=int(simulation_raw.get("seed", 42)),
        sink=str(simulation_raw.get("sink", "stdout")),
    )

    farms: List[FarmConfig] = []
    for farm in raw.get("farms", []):
        farms.append(
            FarmConfig(
                id=str(farm["id"]),
                name=str(farm.get("name", farm["id"])),
                lat=float(farm["lat"]),
                lon=float(farm["lon"]),
                areas=_parse_areas(farm.get("areas", [])),
            )
        )

    if not farms:
        raise ValueError("Config must include at least one farm")

    return Config(simulation=simulation, farms=farms)
