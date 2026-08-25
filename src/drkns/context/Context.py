# noqa: N999
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus


class _Context:

    def __init__(self) -> None:
        self.cached_execution_status: dict[str, StepExecutionStatus] = {}


context: _Context = _Context()
