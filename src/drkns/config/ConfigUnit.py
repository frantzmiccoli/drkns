import os
from checksumdir import dirhash
from hashlib import md5
from typing import Optional, Collection, Dict
from paver.easy import sh, BuildFailure


from drkns.exception import UnknownStepException
from drkns.runner.StepExecutionStatus import StepExecutionStatus


class ConfigUnit:

    def __init__(self, name: str, data: dict):
        self.name: str = name
        self.directory: Optional[str] = data.get('directory', None)
        self.steps: Dict[str: str] = data.get('steps', {})
        self.dependencies: Dict[str: ConfigUnit] = {}

        self._steps_execution_status: Dict[str, StepExecutionStatus] = {}

        self._hash: Optional[str] = None

    def get_hash(self) -> str:
        if self._hash is None:
            self._hash = self._get_computed_hash()

        return self._hash

    def get_error_string(self) -> Optional[str]:
        errors = self._get_errors()

        if len(errors) == 0:
            return None

        return 'Error in "' + self.name + '":\n' + '\n\t'.join(errors) + '\n\n'

    def run_step(self, step_name: str) -> StepExecutionStatus:
        failed_previous_execution_status = self._get_step_run_check(step_name)

        if failed_previous_execution_status is not None:
            output = 'Previous failure of ' \
                     + failed_previous_execution_status.step_name
            return StepExecutionStatus(step_name, False, output)

        command = '(cd "' + self.directory + '"; \n' + self.steps[step_name] + \
                  '\n)'

        output = None
        try:
            output = sh(command, capture=True)
            successful = True
        except BuildFailure:
            successful = False

        step_execution_status = \
            StepExecutionStatus(step_name, successful, output)
        self._steps_execution_status[step_name] = step_execution_status

        return step_execution_status

    def _get_step_run_check(self, target_step_name: str)\
            -> Optional[StepExecutionStatus]:
        for step_name in self.steps.keys():

            if not (step_name in self._steps_execution_status):
                # missing intermediate step
                self.run_step(step_name)

            step_execution_status = self._steps_execution_status[step_name]
            if not step_execution_status.successful:
                return step_execution_status

            if step_name == target_step_name:
                return None

        message = 'Unknown step ' + target_step_name + ' in ' + self.name
        raise UnknownStepException(message)

    def _get_computed_hash(self) -> str:
        hash_input = dirhash(self.directory)

        for dependency_config_unit in self.dependencies:
            hash_input += dependency_config_unit

        hashed = hash_input[0:7] + '-' +\
            md5(hash_input.encode('utf-8')).hexdigest()
        return hashed

    def _get_errors(self) -> Collection[str]:
        errors = []
        if self.directory is None:
            errors.append(self.name + ': directory is not set')
        elif not os.path.exists(self.directory):
            errors.append(self.name + ': directory does not exist')
        if len(self.steps) == 0:
            errors.append(self.name + ': no steps are defined')

        for name, dependency in self.dependencies.items():
            dependency_error_string = dependency.get_error_string()
            if dependency_error_string is not None:
                errors = dependency_error_string

        return errors
