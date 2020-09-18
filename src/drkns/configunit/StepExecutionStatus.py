from datetime import datetime

from typing import Optional


class StepExecutionStatus:

    def __init__(
            self,
            step_name: str,
            output: str,
            successful: bool = False,
            ignored: bool = False
    ):
        self.step_name: str = step_name
        self.successful: bool = successful
        self.ignored: bool = ignored
        self.output: str = output

        self.restored: bool = False

        self.datetime: datetime = datetime.now()
