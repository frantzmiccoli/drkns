from datetime import datetime
import os
from typing import Optional

import drkns.step.step_type

_cwd = os.getcwd()


class StepExecutionStatus:

    def __init__(
            self,
            config_unit_name: str,
            step_name: str,
            output: str,
            successful: bool = False,
            ignored: bool = False,
            step_type: str = drkns.step.step_type.CHECK
    ):
        self.config_unit_name: str = config_unit_name
        self.step_name: str = step_name
        self.successful: bool = successful
        self.ignored: bool = ignored
        self.step_type: str = step_type
        self.output: str = output

        self.restored: bool = False

        self.datetime: datetime = datetime.now()

    def name(self) -> str:
        return self.config_unit_name + '@' + self.step_name
