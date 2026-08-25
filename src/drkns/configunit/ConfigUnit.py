# noqa: N999
import os
from subprocess import Popen

import drkns.step.step_type
from drkns.exception import UnexpectedBranchException
from drkns.step.Step import Step


class ConfigUnit:

    @staticmethod
    def _step_from_raw_steps(raw_steps: dict[str, str | dict]) \
            -> dict[str, Step]:
        return {
            name: Step(command)
            for name, command in raw_steps.items()
        }

    def __init__(
            self,
            name: str,
            data: dict,
            ignored: list[str]
    ):
        self.name: str = name
        self.directory: str = data.get('directory', os.path.abspath('.'))

        self.check_steps: dict[str, Step] = \
            self._step_from_raw_steps(data.get('checkSteps', {}))
        self.build_steps: dict[str, Step] = \
            self._step_from_raw_steps(data.get('buildSteps', {}))
        self.cleanup_steps: dict[str, Step] = \
            self._step_from_raw_steps(data.get('cleanupSteps', {}))

        self.dependencies: list[ConfigUnit] = data.get('dependencies', [])

        self.ignored: list[str] = ignored

        self.hash: str | None = None

        self.pending_subprocesses: list[Popen] = []

    def __eq__(self, other):
        return self.name == other.name

    def get_dependency(self, dependency_name: str) -> 'ConfigUnit | None':
        for dependency in self.dependencies:
            if dependency.name == dependency_name:
                return dependency

        return None

    def get_steps(self, step_type: str) -> dict[str, Step]:
        drkns.step.step_type.check_step_type(step_type)

        if step_type == drkns.step.step_type.CHECK:
            return self.check_steps
        if step_type == drkns.step.step_type.BUILD:
            return self.build_steps
        if step_type == drkns.step.step_type.CLEANUP:
            return self.cleanup_steps

        raise UnexpectedBranchException('Must have return something by now')
