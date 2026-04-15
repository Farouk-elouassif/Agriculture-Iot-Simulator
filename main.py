from __future__ import annotations

import argparse

from simulator.config import load_config
from simulator.engine import SimulationEngine
from simulator.sinks.file_spool_sink import FileSpoolEventSink
from simulator.sinks.stdout_sink import StdoutEventSink


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agriculture IoT Simulator")
    parser.add_argument("--config", default="simulator_config.yaml", help="Path to simulator yaml config")
    parser.add_argument("--sink", default=None, choices=["stdout", "file"], help="Override configured sink")
    parser.add_argument("--spool-dir", default="./spool", help="Directory for file sink output")
    return parser.parse_args()


def build_sink(sink_name: str, spool_dir: str):
    if sink_name == "file":
        return FileSpoolEventSink(directory=spool_dir)
    return StdoutEventSink()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    selected_sink = args.sink or config.simulation.sink
    sink = build_sink(selected_sink, args.spool_dir)
    engine = SimulationEngine(config=config, sink=sink)
    engine.run_forever()


if __name__ == "__main__":
    main()
