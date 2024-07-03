from typing import Collection, Optional
import sys
import os

from drkns.exception import (UnexpectedBranchException, MissingCommandException,
    UnknownCommandException, MissingSyncDirectionException,
    MissingS3PathException, UnknownCommandFlagException,
    MissingForgetTargetException)
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.load import load
from drkns.configunit.get_error_string import get_error_string
from drkns.context.clean_persistence_files import clean_persistence_files
from drkns.context.sync import sync_in, sync_out
from drkns.context.forget import forget
from drkns.runner.run import run
from drkns.runner.get_execution_plan import get_execution_plan
from drkns.runner.get_dependency_groups_configuration \
    import get_dependency_groups_configuration
from drkns.generation.templateloading.get_generation_template \
    import get_generation_template
from drkns.generation.generation.get_formatted_from_groups_configuration \
    import get_formatted_from_groups_configuration
from drkns.debug.get_debug_information import get_debug_information


class Cli:

    def __init__(self) -> None:
        self._args: Collection[str] = []
        self._command: Optional[str] = None
        self._force_success: bool = False
        self._summary: bool = False
        self._limit_output: bool = False
        self._delete: bool = False

    def handle(self) -> None:
        self._parse_args()

        if self._command is None:
            raise UnexpectedBranchException('No command has been parsed')

        check_command = 'check'
        if self._command == check_command:
            self._check()
            return

        clean_command = 'clean'
        if self._command == clean_command:
            self._clean()
            return

        debug_command = 'debug'
        if self._command == debug_command:
            self._debug()
            return

        forget_command = 'forget'
        if self._command == forget_command:
            self._forget()
            return

        list_command = 'list'
        if self._command == list_command:
            self._list()
            return

        run_command = 'run'
        if self._command == run_command:
            self._run()
            return

        sync_command = 'sync'
        if self._command == sync_command:
            self._sync()
            return

        generate_command = 'generate'
        if self._command == generate_command:
            self._generate()
            return

        allowed_commands = [
            check_command, clean_command, debug_command, forget_command,
            list_command, run_command, sync_command, generate_command
        ]

        message = 'Unkown command: ' + self._command +\
                  '. Allowed commands are "' + '", "'.join(allowed_commands) + \
                  '".'
        raise UnknownCommandException(message)

    def _parse_args(self):
        provided_args = sys.argv[1:]
        if len(provided_args) == 0:
            raise MissingCommandException()

        self._command = provided_args.pop(0)

        force_success_flag = '--force-success'
        if force_success_flag in provided_args:
            index = provided_args.index(force_success_flag)
            provided_args.pop(index)
            self._force_success = True

        summary_flag = '--summary'
        if summary_flag in provided_args:
            index = provided_args.index(summary_flag)
            provided_args.pop(index)
            self._summary = True

        limit_output_flag = '--limit-output'
        if limit_output_flag in provided_args:
            index = provided_args.index(limit_output_flag)
            provided_args.pop(index)
            self._limit_output = True

        delete_flag = '--delete'
        if delete_flag in provided_args:
            index = provided_args.index(delete_flag)
            provided_args.pop(index)
            self._delete = True

        for arg in provided_args:
            if arg.find('--') != -1:
                allowed_flags = [
                    force_success_flag, summary_flag, limit_output_flag,
                    delete_flag
                ]

                message = 'Unkown command flag: ' + arg + \
                          '. Allowed flags are "' + \
                          '", "'.join(allowed_flags) + '".'
                raise UnknownCommandFlagException(message)

        self._args = provided_args

    def _check(self):
        config_unit = self._get_config_unit()
        error_string = get_error_string(config_unit)

        if error_string is None:
            sys.exit()

        sys.exit(error_string)

    # noinspection PyMethodMayBeStatic
    def _clean(self):
        clean_persistence_files()
        sys.exit()

    def _debug(self):
        config_unit = self._get_config_unit()
        print(get_debug_information(config_unit))
        sys.exit()

    def _forget(self):
        if len(self._args) != 1:
            error_message = 'Missing forget target. Allowed targets are a ' +\
                'unit name, "main" and "all".'
            raise MissingForgetTargetException(error_message)

        unit_name = self._args[0]
        if unit_name == 'all':
            unit_name = None

        forget(unit_name)

    def _list(self):
        config_unit = self._get_config_unit()
        execution_plan = get_execution_plan(config_unit)
        step_names = \
            [prefixed_step_name for _, _, prefixed_step_name in execution_plan]
        print('\n'.join(step_names))

    def _run(self):
        config_unit = self._get_config_unit()

        target = None
        if len(self._args) > 0:
            target = self._args[0]

        successful, output_lines = run(config_unit, target,
                                       self._summary, self._limit_output)
        if len(output_lines) > 0:
            print('\n'.join(output_lines))
        if successful or self._force_success:
            sys.exit()

        sys.exit(1)

    def _sync(self):
        if (len(self._args) < 1) \
                or (self._args[0] not in ['in', 'out']):
            message = 'Sync direction should be in or out'
            raise MissingSyncDirectionException(message)

        sync_direction = self._args[0]

        environment_variable_name = 'DRKNS_S3_PATH'
        target_s3_path = os.environ.get(environment_variable_name)
        if len(self._args) == 2:
            target_s3_path = self._args[1]

        if target_s3_path is None:
            message = 'Missing s3 path, it can be provided as an argument or ' \
                      'an environment variable: ' + environment_variable_name
            raise MissingS3PathException(message)

        if sync_direction == 'in':
            (return_code, output) = sync_in(target_s3_path)
        else:
            (return_code, output) = sync_out(target_s3_path, self._delete)

        successful = return_code == 0

        if not successful:
            print(output)

        sys.exit(return_code)

    def _generate(self):
        config_unit = self._get_config_unit()
        generation_template = get_generation_template('.')
        groups_configuration = get_dependency_groups_configuration(config_unit)
        generated = get_formatted_from_groups_configuration(
            generation_template,
            groups_configuration)
        print(generated)

    # noinspection PyMethodMayBeStatic
    def _get_config_unit(self) -> ConfigUnit:
        return load('drkns.yml')
