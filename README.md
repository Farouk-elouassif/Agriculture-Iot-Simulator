# Agriculture IoT Simulator

Realistic but simple IoT farm data generator in Python.

## Goals

- Keep configuration minimal.
- Use farm latitude and longitude.
- Use live weather to make generated data more realistic.
- Emit JSON events for ingestion pipelines (Flume, files, stdout).

## Quick Start

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Update `simulator_config.yaml` with your farms and coordinates.
3. Run the generator (entrypoint added in later feature commits):

   ```bash
   python main.py --config simulator_config.yaml
   ```

## Run Modes

- Stream to stdout (default):

   ```bash
   python main.py --config simulator_config.yaml --sink stdout
   ```

- Write newline-delimited JSON to spool file:

   ```bash
   python main.py --config simulator_config.yaml --sink file --spool-dir ./spool
   ```

## Realism Logic

- Weather is fetched by farm coordinates from Open-Meteo.
- If weather API fails, cached weather or fallback values are used.
- Soil moisture reacts to heat, wind, irrigation, and rain.
- Irrigation toggles automatically using moisture thresholds and rain conditions.
- Device battery and signal drift gradually over time.

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

