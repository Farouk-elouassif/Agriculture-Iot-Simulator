import random
import unittest

from simulator.models import WeatherSnapshot
from simulator.soil_model import SoilModelService


class SoilModelTests(unittest.TestCase):
    def test_rain_and_irrigation_raise_moisture(self):
        rng = random.Random(1)
        svc = SoilModelService(rng)
        weather = WeatherSnapshot(
            air_temperature=30.0,
            humidity=50.0,
            pressure=1010.0,
            wind_speed=10.0,
            wind_direction="NW",
            rain_detected=True,
            rain_intensity=4.0,
            light_lux=10000.0,
            uv_index=6.0,
            source="test",
        )
        previous = {
            "ph": 6.4,
            "moisture": 40.0,
            "temperature": 22.0,
            "ec": 1.2,
            "nitrogen": 45.0,
            "phosphorus": 30.0,
            "potassium": 50.0,
            "organic_matter": 3.0,
            "salinity": 0.8,
        }

        next_soil = svc.next_soil("tomato", weather, previous, irrigation_on=True)
        self.assertGreater(next_soil["moisture"], 40.0)


if __name__ == "__main__":
    unittest.main()
