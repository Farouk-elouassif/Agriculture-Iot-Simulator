from dataclasses import dataclass
from typing import List


@dataclass
class AreaConfig:
    id: str
    crop: str
    devices: List[str]


@dataclass
class FarmConfig:
    id: str
    name: str
    lat: float
    lon: float
    areas: List[AreaConfig]


@dataclass
class SimulationConfig:
    event_interval_seconds: int = 5
    weather_refresh_minutes: int = 15
    seed: int = 42
    sink: str = "stdout"


@dataclass
class Config:
    simulation: SimulationConfig
    farms: List[FarmConfig]


@dataclass
class WeatherSnapshot:
    air_temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: str
    rain_detected: bool
    rain_intensity: float
    light_lux: float
    uv_index: float
    source: str = "live"

