import os
from dirhash import dirhash
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
        self.dependencies: Dict[str: ConfigUnit] = data.get('dependencies', {})

        self._steps_execution_status: Dict[str, StepExecutionStatus] = {}

        self._hash: Optional[str] = None

    def get_hash(self) -> str:
        if self._hash is None:
            self._hash = self._get_computed_hash()

        return self._hash

    def get_error_string(self, indent: Optional[int]=None) -> Optional[str]:
        if indent is None:
            indent = 0

        errors = self._get_errors(indent + 1)

        if len(errors) == 0:
            return None

        original_indent_string = '   ' * indent
        indent_string = '   ' * (indent + 1)
        return original_indent_string + 'Error in "' + self.name + '":\n' +\
            indent_string + ('\n' + indent_string).join(errors) + '\n\n'

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

    def get_steps(self, ignore_dependency: bool = False) \
            -> Collection[str]:
        """
        In proper execution order
        :param ignore_dependency:
        :return:
        """
        steps = []

        considered_prefixes_and_config_units = [(None, self)]

        while len(considered_prefixes_and_config_units) != 0:
            current_prefix, config_unit = \
                considered_prefixes_and_config_units.pop(0)

            for dependency_name in config_unit.dependencies.keys():
                if ignore_dependency:
                    break

                prefix = dependency_name + '.'

                if current_prefix is not None:
                    prefix = current_prefix + prefix

                prefix_and_config_unit = \
                    (prefix, config_unit.dependencies[dependency_name])
                considered_prefixes_and_config_units.append(
                    prefix_and_config_unit)

            if current_prefix is None:
                current_prefix = ''

            unit_steps = [current_prefix + step_name
                          for step_name in config_unit.steps.keys()]
            steps = unit_steps + steps

        return steps

    def _get_step_run_check(self, target_step_name: str)\
            -> Optional[StepExecutionStatus]:
        for step_name in self.steps.keys():
            if step_name == target_step_name:
                return None

            if not (step_name in self._steps_execution_status):
                # missing intermediate step
                self.run_step(step_name)

            step_execution_status = self._steps_execution_status[step_name]
            if not step_execution_status.successful:
                return step_execution_status

        message = 'Unknown step ' + target_step_name + ' in ' + self.name
        raise UnknownStepException(message)

    def _get_computed_hash(self) -> str:
        hash_input = \
            dirhash(self.directory, 'sha1', ignore=[".*", ".*/"])

        for dependency_config_unit in self.dependencies:
            hash_input += dependency_config_unit

        hashed = hash_input[0:7] + '-' +\
            md5(hash_input.encode('utf-8')).hexdigest()
        return hashed

    def _get_errors(self, indent) -> Collection[str]:
        errors = []
        if self.directory is None:
            errors.append(self.name + ': directory is not set')
        elif not os.path.exists(self.directory):
            errors.append(self.name + ': directory does not exist')
        if (len(self.steps) == 0) and (len(self.dependencies) == 0):
            errors.append(self.name + ': no steps nor dependencies are defined')

        for name, dependency in self.dependencies.items():
            dependency_error_string = dependency.get_error_string(indent)
            if dependency_error_string is not None:
                errors = dependency_error_string

        return errors
