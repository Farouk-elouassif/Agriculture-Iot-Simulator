from __future__ import annotations

import json
from typing import Dict

from simulator.sinks.base import EventSink


class StdoutEventSink(EventSink):
    def emit(self, payload: Dict[str, object]) -> None:
        print(json.dumps(payload, separators=(",", ":"), ensure_ascii=True), flush=True)
