from __future__ import annotations

import random
import time
from typing import Dict, Tuple

from simulator.device_health import DeviceHealthService, DeviceHealthState
from simulator.irrigation import IrrigationService
from simulator.models import AreaConfig, Config
from simulator.payload_builder import SensorPayloadBuilder
from simulator.sinks.base import EventSink
from simulator.soil_model import SoilModelService
from simulator.weather_cache import WeatherCacheService


class SimulationEngine:
    def __init__(self, config: Config, sink: EventSink) -> None:
        self.config = config
        self.sink = sink

        self.rng = random.Random(config.simulation.seed)
        self.weather_cache = WeatherCacheService(config.simulation.weather_refresh_minutes)
        self.soil_model = SoilModelService(self.rng)
        self.irrigation_service = IrrigationService()
        self.device_health_service = DeviceHealthService(self.rng)
        self.payload_builder = SensorPayloadBuilder()

        self._soil_state: Dict[Tuple[str, str], Dict[str, float]] = {}
        self._irrigation_state: Dict[Tuple[str, str], bool] = {}
        self._device_health_state: Dict[str, DeviceHealthState] = {}

    def _next_area_payloads(self) -> list[dict]:
        payloads: list[dict] = []

        for farm in self.config.farms:
            weather = self.weather_cache.get_weather(farm)

            for area in farm.areas:
                key = (farm.id, area.id)
                prev_soil = self._soil_state.get(key)
                irrigation_on = self._irrigation_state.get(key, False)
                current_moisture = prev_soil["moisture"] if prev_soil else 65.0
                irrigation_on = self.irrigation_service.decide_status(current_moisture, weather, irrigation_on)

                soil = self.soil_model.next_soil(area.crop, weather, prev_soil, irrigation_on)
                self._soil_state[key] = soil
                self._irrigation_state[key] = irrigation_on

                payloads.extend(self._device_payloads(farm, area, weather, soil, irrigation_on))

        return payloads

    def _device_payloads(
        self,
        farm,
        area: AreaConfig,
        weather,
        soil: Dict[str, float],
        irrigation_on: bool,
    ) -> list[dict]:
        payloads: list[dict] = []
        for device_id in area.devices:
            state = self._device_health_state.setdefault(device_id, DeviceHealthState())
            next_state = self.device_health_service.next_state(state, weather)
            health_snapshot = self.device_health_service.snapshot(next_state, weather)

            payload = self.payload_builder.build(
                device_id=device_id,
                farm=farm,
                area=area,
                weather=weather,
                soil=soil,
                irrigation_on=irrigation_on,
                device_health=health_snapshot,
            )
            payloads.append(payload)
        return payloads

    def run_forever(self) -> None:
        interval = max(1, self.config.simulation.event_interval_seconds)
        while True:
            for payload in self._next_area_payloads():
                self.sink.emit(payload)
            time.sleep(interval)
