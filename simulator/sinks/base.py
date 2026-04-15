from __future__ import annotations

from typing import Dict


class EventSink:
    def emit(self, payload: Dict[str, object]) -> None:
        raise NotImplementedError
