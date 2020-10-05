import os
from typing import Optional, Union, Dict

from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.configunit.Step import Step


class ConfigUnit:

    def __init__(self, name: str, data: dict):
        self.name: str = name
        self.directory: str = data.get('directory', os.path.abspath('.'))

        self.steps: Dict[str, Step] = \
            self._step_from_raw_steps(data.get('steps', {}))
        self.cleanupSteps: Dict[str, Step] = \
            self._step_from_raw_steps(data.get('cleanupSteps', {}))

        self.dependencies: Dict[str, ConfigUnit] = data.get('dependencies', {})

        self.hash: Optional[str] = None

    @staticmethod
    def _step_from_raw_steps(raw_steps: Dict[str, Union[str, Dict]]) \
            -> Dict[str, Step]:
        return {
            name: Step(command)
            for name, command in raw_steps.items()
        }