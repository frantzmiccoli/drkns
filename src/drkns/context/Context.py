from typing import Dict

from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus


class _Context:

    def __init__(self) -> None:
        self.cached_execution_status: Dict[str, StepExecutionStatus] = {}


context: _Context = _Context()
