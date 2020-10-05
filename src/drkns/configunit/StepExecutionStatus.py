from datetime import datetime
import os
from typing import Optional

_cwd = os.getcwd()


class StepExecutionStatus:

    def __init__(
            self,
            config_unit_name: str,
            step_name: str,
            output: str,
            successful: bool = False,
            ignored: bool = False,
            cleanup: bool = False
    ):
        self.config_unit_name: str = config_unit_name
        self.step_name: str = step_name
        self.successful: bool = successful
        self.ignored: bool = ignored
        self.cleanup: bool = cleanup
        self.output: str = output

        self.restored: bool = False

        self.datetime: datetime = datetime.now()

    def name(self) -> str:
        return self.config_unit_name + '@' + self.step_name
        #print(self.directory)
        #name = self.directory.replace(_cwd, '')
        #name += '@'
        #if self.cleanup:
        #    name += 'cleanup/'

        #name += self.step_name

        #return name
