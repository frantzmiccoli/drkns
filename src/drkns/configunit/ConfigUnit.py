from typing import Optional, Union, Dict

from drkns.configunit.StepExecutionStatus import StepExecutionStatus
from drkns.configunit.Step import Step


class ConfigUnit:

    def __init__(self, name: str, data: dict):
        self.name: str = name
        self.directory: str = data.get('directory', '.')

        raw_steps: Dict[str, Union[str, Dict]] = data.get('steps', {})
        self.steps: Dict[str, Step] = {
            name: Step(command)
            for name, command in raw_steps.items()
        }

        self.dependencies: Dict[str, ConfigUnit] = data.get('dependencies', {})

        self.hash: Optional[str] = None
