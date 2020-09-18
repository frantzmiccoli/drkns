from typing import Optional, Dict

from drkns.configunit.StepExecutionStatus import StepExecutionStatus


class ConfigUnit:

    def __init__(self, name: str, data: dict):
        self.name: str = name
        self.directory: str = data.get('directory', '.')
        self.steps: Dict[str, str] = data.get('steps', {})
        self.dependencies: Dict[str, ConfigUnit] = data.get('dependencies', {})

        self.hash: Optional[str] = None
