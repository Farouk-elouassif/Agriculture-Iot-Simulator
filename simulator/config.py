from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from simulator.models import AreaConfig, Config, FarmConfig, SimulationConfig


def _generate_device_ids(farm_id: str, area_id: str, sensor_count: int) -> List[str]:
    return [f"{farm_id}_{area_id}_DEV_{idx:03d}" for idx in range(1, sensor_count + 1)]


def _parse_areas(farm_id: str, raw_areas: List[Dict[str, Any]]) -> List[AreaConfig]:
    areas: List[AreaConfig] = []
    for area in raw_areas:
        area_id = str(area["id"])
        area_size_km2 = float(area.get("area_size_km2", 1.0))
        if area_size_km2 <= 0:
            raise ValueError(f"Area '{area_id}' in farm '{farm_id}' must have area_size_km2 > 0")

        devices = [str(device_id) for device_id in area.get("devices", [])]
        sensor_count = int(area.get("sensor_count", len(devices) if devices else 1))
        if sensor_count <= 0:
            raise ValueError(f"Area '{area_id}' in farm '{farm_id}' must have sensor_count > 0")

        if devices and len(devices) != sensor_count:
            raise ValueError(
                f"Area '{area_id}' in farm '{farm_id}' has sensor_count={sensor_count} "
                f"but devices list has {len(devices)} entries"
            )

        if not devices:
            devices = _generate_device_ids(farm_id=farm_id, area_id=area_id, sensor_count=sensor_count)

        areas.append(
            AreaConfig(
                id=area_id,
                crop=str(area["crop"]).lower(),
                area_size_km2=area_size_km2,
                sensor_count=sensor_count,
                devices=devices,
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
                areas=_parse_areas(str(farm["id"]), farm.get("areas", [])),
            )
        )

    if not farms:
        raise ValueError("Config must include at least one farm")

    return Config(simulation=simulation, farms=farms)
