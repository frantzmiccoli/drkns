from typing import Optional, Dict

from drkns.configunit.StepExecutionStatus import StepExecutionStatus


class ConfigUnit:

    def __init__(self, name: str, data: dict):
        self.name: str = name
        self.directory: Optional[str] = data.get('directory', None)
        self.steps: Dict[str: str] = data.get('steps', {})
        self.dependencies: Dict[str: ConfigUnit] = data.get('dependencies', {})

        self.steps_execution_status: Dict[str, StepExecutionStatus] = {}

        self.hash: Optional[str] = None

        self.execution_history: Dict[str, StepExecutionStatus] = {}
