from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from simulator.sinks.base import EventSink


class FileSpoolEventSink(EventSink):
    def __init__(self, directory: str = "./spool") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.file_path = self.directory / "events.jsonl"

    def emit(self, payload: Dict[str, object]) -> None:
        with self.file_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
