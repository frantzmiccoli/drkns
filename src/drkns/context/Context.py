from datetime import datetime

from typing import Dict


class _Context:

    def __init__(self):
        self.cached_execution_dates: Dict[str, datetime] = {}


context: _Context = _Context()
