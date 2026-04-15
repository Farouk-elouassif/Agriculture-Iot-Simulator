import unittest

from simulator.models import AreaConfig, FarmConfig, WeatherSnapshot
from simulator.payload_builder import SensorPayloadBuilder


class PayloadBuilderTests(unittest.TestCase):
    def test_payload_contains_required_sections(self):
        builder = SensorPayloadBuilder()
        farm = FarmConfig(id="F1", name="Farm", lat=30.0, lon=31.0, areas=[])
        area = AreaConfig(id="A1", crop="tomato", devices=["D1"])
        weather = WeatherSnapshot(
            air_temperature=26.0,
            humidity=60.0,
            pressure=1012.0,
            wind_speed=7.0,
            wind_direction="N",
            rain_detected=False,
            rain_intensity=0.0,
            light_lux=12000.0,
            uv_index=6.0,
            source="live",
        )
        soil = {
            "ph": 6.4,
            "moisture": 67.0,
            "temperature": 23.5,
            "ec": 1.3,
            "nitrogen": 44.0,
            "phosphorus": 29.0,
            "potassium": 49.0,
            "organic_matter": 3.1,
            "salinity": 0.8,
        }
        health = {"battery": 80.0, "signal_strength": -66.0, "internal_temp": 40.0}

        payload = builder.build(
            device_id="D1",
            farm=farm,
            area=area,
            weather=weather,
            soil=soil,
            irrigation_on=True,
            device_health=health,
        )

        self.assertIn("soil", payload)
        self.assertIn("environment", payload)
        self.assertIn("light", payload)
        self.assertIn("device_health", payload)
        self.assertEqual(payload["farm_location"]["lat"], 30.0)
        self.assertEqual(payload["water_system"]["irrigation_status"], "ON")


if __name__ == "__main__":
    unittest.main()
