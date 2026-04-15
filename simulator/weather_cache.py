from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

from simulator.models import FarmConfig, WeatherSnapshot
from simulator.weather_client import OpenMeteoClient, default_weather


class WeatherCacheService:
    def __init__(self, refresh_minutes: int, client: OpenMeteoClient | None = None) -> None:
        self.refresh_minutes = refresh_minutes
        self.client = client or OpenMeteoClient()
        self._cache: Dict[str, Tuple[datetime, WeatherSnapshot]] = {}

    def get_weather(self, farm: FarmConfig) -> WeatherSnapshot:
        now = datetime.now(tz=timezone.utc)
        cached = self._cache.get(farm.id)

        if cached and now - cached[0] < timedelta(minutes=self.refresh_minutes):
            return cached[1]

        try:
            snapshot = self.client.fetch(farm.lat, farm.lon)
        except Exception:
            # Keep simulation alive by using previous snapshot or a default baseline.
            snapshot = cached[1] if cached else default_weather()

        self._cache[farm.id] = (now, snapshot)
        return snapshot
