from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from simulator.models import AreaConfig, FarmConfig, WeatherSnapshot


def _epoch_seconds() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


class SensorPayloadBuilder:
    def build(
        self,
        device_id: str,
        farm: FarmConfig,
        area: AreaConfig,
        weather: WeatherSnapshot,
        soil: Dict[str, float],
        irrigation_on: bool,
        device_health: Dict[str, float],
    ) -> Dict[str, object]:
        flow_rate = 3.5 if irrigation_on else 0.0
        water_level = 72.0 - (0.2 if irrigation_on else 0.0)

        return {
            "schema_version": 1,
            "weather_source": weather.source,
            "device_id": device_id,
            "farm_id": farm.id,
            "area_id": area.id,
            "crop": area.crop,
            "farm_location": {"lat": farm.lat, "lon": farm.lon},
            "timestamp": _epoch_seconds(),
            "soil": soil,
            "water_system": {
                "water_level": round(water_level, 2),
                "flow_rate": round(flow_rate, 2),
                "irrigation_status": "ON" if irrigation_on else "OFF",
            },
            "environment": {
                "air_temperature": round(weather.air_temperature, 2),
                "humidity": round(weather.humidity, 2),
                "pressure": round(weather.pressure, 2),
                "rain_detected": weather.rain_detected,
                "rain_intensity": round(weather.rain_intensity, 2),
                "wind_speed": round(weather.wind_speed, 2),
                "wind_direction": weather.wind_direction,
            },
            "light": {
                "lux": round(weather.light_lux, 2),
                "uv_index": round(weather.uv_index, 2),
            },
            "device_health": device_health,
        }
