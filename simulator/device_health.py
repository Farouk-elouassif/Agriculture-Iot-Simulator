from __future__ import annotations

import random
from dataclasses import dataclass

from simulator.models import WeatherSnapshot


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class DeviceHealthState:
    battery: float = 100.0
    signal_strength: float = -65.0


class DeviceHealthService:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def next_state(self, state: DeviceHealthState, weather: WeatherSnapshot) -> DeviceHealthState:
        battery_drop = self.rng.uniform(0.01, 0.06)
        signal_jitter = self.rng.uniform(-1.8, 1.8)

        state.battery = _clamp(state.battery - battery_drop, 5.0, 100.0)
        state.signal_strength = _clamp(state.signal_strength + signal_jitter, -110.0, -40.0)

        return state

    def snapshot(self, state: DeviceHealthState, weather: WeatherSnapshot) -> dict:
        internal_temp = weather.air_temperature + self.rng.uniform(8.0, 16.0)
        return {
            "battery": round(state.battery, 2),
            "signal_strength": round(state.signal_strength, 2),
            "internal_temp": round(internal_temp, 2),
        }
