# noqa: N999

import os
from datetime import UTC, datetime

import drkns.step.step_type

_cwd = os.getcwd()


class StepExecutionStatus:

    # Fallback for objects unpickled from a persisted cache written before
    # this attribute existed.
    duration: float | None = None

    def __init__(
        self,
        config_unit_name: str,
        step_name: str,
        output: str,
        successful: bool = False,
        ignored: bool = False,
        step_type: str = drkns.step.step_type.CHECK,
        hash: str | None = None,
        duration: float | None = None
    ):
        self.config_unit_name: str = config_unit_name
        self.step_name: str = step_name
        self.successful: bool = successful
        self.ignored: bool = ignored
        self.step_type: str = step_type
        self.output: str = output

        self.hash: str | None = hash
        self.duration: float | None = duration
        self.restored: bool = False

        self.datetime: datetime = datetime.now(UTC)

    def name(self) -> str:
        return self.config_unit_name + '@' + self.step_name
