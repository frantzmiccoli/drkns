import os
from subprocess import Popen
from typing import Optional, Union, Dict, List

from drkns.step.Step import Step
import drkns.step.step_type


class ConfigUnit:

    @staticmethod
    def _step_from_raw_steps(raw_steps: Dict[str, Union[str, Dict]]) \
            -> Dict[str, Step]:
        return {
            name: Step(command)
            for name, command in raw_steps.items()
        }

    def __init__(
            self,
            name: str,
            data: dict,
            ignored: List[str]
            ):
        self.name: str = name
        self.directory: str = data.get('directory', os.path.abspath('.'))

        self.check_steps: Dict[str, Step] = \
            self._step_from_raw_steps(data.get('checkSteps', {}))
        self.build_steps: Dict[str, Step] = \
            self._step_from_raw_steps(data.get('buildSteps', {}))
        self.cleanup_steps: Dict[str, Step] = \
            self._step_from_raw_steps(data.get('cleanupSteps', {}))

        self.dependencies: List[ConfigUnit] = data.get('dependencies', [])

        self.ignored: List[str] = ignored

        self.hash: Optional[str] = None

        self.pending_subprocesses: List[Popen] = []

    def __eq__(self, other):
        return self.name == other.name

    def get_dependency(self, dependency_name: str) -> Optional['ConfigUnit']:
        for dependency in self.dependencies:
            if dependency.name == dependency_name:
                return dependency

        return None

    def get_steps(self, step_type: str) -> Dict[str, Step]:
        drkns.step.step_type.check_step_type(step_type)

        if step_type == drkns.step.step_type.CHECK:
            return self.check_steps
        if step_type == drkns.step.step_type.BUILD:
            return self.build_steps
        if step_type == drkns.step.step_type.CLEANUP:
            return self.cleanup_steps

        raise Exception('Must have return something by now')
