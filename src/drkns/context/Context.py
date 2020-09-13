from typing import Dict

from drkns.configunit.StepExecutionStatus import StepExecutionStatus


class _Context:

    def __init__(self):
        self.cached_execution_status: Dict[str, StepExecutionStatus] = {}


context: _Context = _Context()
