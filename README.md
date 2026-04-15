# Agriculture IoT Simulator

Realistic, configurable IoT farm telemetry simulator in Python.

This project generates farm sensor events that mimic real-world behavior using:

- Farm coordinates (latitude/longitude)
- Live weather data (Open-Meteo)
- Crop-aware soil baselines
- Time-evolving soil, irrigation, and device health dynamics

It is designed to feed data engineering pipelines such as:

Sensor Nodes -> Flume -> HDFS (Data Lake) -> Processing Layer -> HBase -> Spring Boot + PostgreSQL + React

## Goals

- Keep configuration simple for fast onboarding.
- Generate realistic telemetry, not only random values.
- Use actual weather by location to increase realism.
- Emit JSON payloads compatible with streaming and lake ingestion workflows.

## Current Features

- Minimal YAML configuration for simulation and topology
- Multi-farm support
- Area-level crop assignment
- Area metadata: area size and sensor count
- Device list support (explicit IDs) or auto-generated device IDs
- Live weather fetch with cache and fallback behavior
- Soil evolution model (moisture, pH, nutrients, salinity, temperature)
- Irrigation auto control based on moisture/rain conditions
- Device health simulation (battery, signal, internal temperature)
- Multiple sinks: stdout and JSONL spool file
- Unit tests for key components

## Project Structure

```text
.
├── main.py
├── simulator_config.yaml
├── requirements.txt
├── simulator/
│   ├── config.py
│   ├── models.py
│   ├── crop_profiles.py
│   ├── weather_client.py
│   ├── weather_cache.py
│   ├── soil_model.py
│   ├── irrigation.py
│   ├── device_health.py
│   ├── payload_builder.py
│   ├── engine.py
│   └── sinks/
│       ├── base.py
│       ├── stdout_sink.py
│       └── file_spool_sink.py
└── tests/
   ├── test_config.py
   ├── test_soil_model.py
   └── test_payload_builder.py
```

## Quick Start

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Update `simulator_config.yaml` with your farm setup.
3. Run the generator:

   ```bash
   python main.py --config simulator_config.yaml
   ```

4. Stop with Ctrl+C.

## Configuration Reference

Example configuration:

```yaml
simulation:
   event_interval_seconds: 5
   weather_refresh_minutes: 15
   seed: 42
   sink: stdout

farms:
   - id: FARM_01
      name: Delta Farm
      lat: 30.0444
      lon: 31.2357
      areas:
         - id: A1
            crop: tomato
            area_size_km2: 15
            sensor_count: 2
            devices:
               - DEV_001
               - DEV_002
         - id: A2
            crop: orange
            area_size_km2: 15
            sensor_count: 1
            devices:
               - DEV_003
```

Field details:

- `simulation.event_interval_seconds`: event emission interval per cycle
- `simulation.weather_refresh_minutes`: weather cache refresh period
- `simulation.seed`: deterministic randomness seed
- `simulation.sink`: default output sink (`stdout` or `file`)
- `farms[].lat/lon`: location used for live weather
- `areas[].area_size_km2`: area size in square kilometers
- `areas[].sensor_count`: expected number of sensor devices in area
- `areas[].devices`: explicit device IDs (optional if auto-generation is preferred)

Validation rules:

- `area_size_km2 > 0`
- `sensor_count > 0`
- If both `sensor_count` and `devices` are provided, counts must match
- If `devices` is omitted, IDs are generated automatically

### Sensor Density Note

`15 km2 = 1500 hectares`.

For real deployments, 1-2 sensors over 1500 ha is typically too sparse. For simulation this is valid, but for agronomy realism you may want a higher count depending on the monitoring resolution you target.

## Run Modes

- Stream to stdout (default):

   ```bash
   python main.py --config simulator_config.yaml --sink stdout
   ```

- Write newline-delimited JSON to spool file:

   ```bash
   python main.py --config simulator_config.yaml --sink file --spool-dir ./spool
   ```

## Event Format

Each device emits one JSON event per cycle. Core sections:

- identity and topology: `device_id`, `farm_id`, `area_id`, `crop`
- location: `farm_location.lat/lon`
- timestamp: epoch seconds
- `soil`: pH, moisture, temperature, EC, NPK, organic matter, salinity
- `water_system`: level, flow rate, irrigation status
- `environment`: air temperature, humidity, pressure, rain, wind
- `light`: lux, UV index
- `device_health`: battery, signal, internal temperature
- metadata: `schema_version`, `weather_source`

## Realism Model

- Weather uses live Open-Meteo values by farm coordinates.
- Cached snapshots reduce API calls and improve stability.
- API failures fallback to cached/default weather to keep generation running.
- Soil moisture decreases with heat and wind, increases with rain/irrigation.
- Soil nutrients drift downward gradually to mimic crop consumption.
- Irrigation toggles by moisture thresholds unless rain suppresses it.
- Device health changes over time with bounded drift.

## Flume / Data Engineering Integration

Recommended ingestion patterns:

- Start with `stdout` sink for local validation.
- Use `file` sink (`events.jsonl`) with Flume spooldir source in integration setups.
- Keep one event per line for reliable parsing and downstream replay.

## Multi-Tenant Recommendation

For production user onboarding:

- Keep YAML for defaults or local testing
- Store per-user/per-farm configurations in PostgreSQL
- Load active simulation configs from DB at runtime

This avoids YAML write contention and scales better with many users.

## Testing

Run tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Troubleshooting

- No weather response:
   - Check internet access
   - Simulator will continue using cached/fallback weather
- Invalid config error:
   - Verify `sensor_count` and `devices` length consistency
   - Ensure `area_size_km2` is positive
- Too much output:
   - Increase `event_interval_seconds`
   - Reduce `sensor_count` or number of areas

## Next Improvements

- Add sink for direct Flume-compatible TCP/HTTP emission
- Add tenant-aware runtime source from PostgreSQL
- Add seasonality profile and day/night light curve improvements
- Add schema registry compatibility and versioning strategy

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

