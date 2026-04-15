import tempfile
import unittest
from pathlib import Path

from simulator.config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_config_parses_farm_and_areas(self):
        yaml_text = """
simulation:
  event_interval_seconds: 2
  weather_refresh_minutes: 10
  seed: 7
  sink: stdout
farms:
  - id: F1
    name: Test Farm
    lat: 30.0
    lon: 31.0
    areas:
      - id: A1
        crop: tomato
        devices: [D1, D2]
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "cfg.yaml"
            path.write_text(yaml_text, encoding="utf-8")

            cfg = load_config(str(path))

        self.assertEqual(cfg.simulation.seed, 7)
        self.assertEqual(len(cfg.farms), 1)
        self.assertEqual(cfg.farms[0].id, "F1")
        self.assertEqual(cfg.farms[0].areas[0].devices, ["D1", "D2"])


if __name__ == "__main__":
    unittest.main()
