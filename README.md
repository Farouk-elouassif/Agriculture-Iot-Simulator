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
