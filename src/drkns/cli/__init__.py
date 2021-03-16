import sys
from typing import Collection
import os

from drkns.exception import MissingCommandException, UnknownCommandException,\
    MissingSyncDirectionException, MissingS3PathException,\
    UnknownCommandFlagException
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.load import load
from drkns.configunit.get_error_string import get_error_string
from drkns.context.clean_persistence_files import clean_persistence_files
from drkns.context.sync import sync_in, sync_out
from drkns.runner.run import run
from drkns.runner.get_execution_plan import get_execution_plan
from drkns.debug.get_debug_information import get_debug_information


class Cli:

    def __init__(self):
        self._args: Collection[str] = []
        self._command: str = None
        self._force_success: bool = False
        self._summary: bool = False
        self._limit_output: bool = False

    def handle(self):
        self._parse_args()

        if self._command == 'check':
            self._check()
            return

        if self._command == 'list':
            self._list()
            return

        if self._command == 'sync':
            self._sync()
            return

        if self._command == 'run':
            self._run()
            return

        if self._command == 'clean':
            self._clean()
            return

        if self._command == 'debug':
            self._debug()
            return

        message = 'Unkown command: ' + self._command +\
                  '. Allowed commands are "run" and "check".'
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

        for arg in provided_args:
            if arg.find('--') != -1:
                message = 'Unkown command flag: ' + arg + \
                          '. Allowed flags are "--force-success".'
                raise UnknownCommandFlagException(message)

        self._args = provided_args

    def _check(self):
        config_unit = self._get_config_unit()
        error_string = get_error_string(config_unit)

        if error_string is None:
            sys.exit()

        sys.exit(error_string)

    def _list(self):
        config_unit = self._get_config_unit()
        execution_plan = get_execution_plan(config_unit)
        step_names = \
            [prefixed_step_name for _, _, prefixed_step_name in execution_plan]
        print('\n'.join(step_names))

    def _sync(self):
        if (len(self._args) < 1) \
                or (self._args[0] not in ['in', 'out']):
            message = 'Sync direction should be in or out'
            raise MissingSyncDirectionException(message)

        sync_direction = self._args[0]

        environment_variable_name = 'DRKNS_S3_PATH'
        target_s3_path = os.environ.get(environment_variable_name)
        if len(self._args) == 3:
            target_s3_path = self._args[1]

        if target_s3_path is None:
            message = 'Missing s3 path, it can be provided as an argument or ' \
                      'an environment variable: ' + environment_variable_name
            raise MissingS3PathException(message)

        if sync_direction == 'in':
            (return_code, output) = sync_in(target_s3_path)
        else:
            (return_code, output) = sync_out(target_s3_path)

        successful = return_code == 0

        if not successful:
            print(output)

        sys.exit(return_code)

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

    # noinspection PyMethodMayBeStatic
    def _clean(self):
        clean_persistence_files()
        sys.exit()

    def _debug(self):
        config_unit = self._get_config_unit()
        print(get_debug_information(config_unit))
        sys.exit()

    # noinspection PyMethodMayBeStatic
    def _get_config_unit(self) -> ConfigUnit:
        return load('drkns.yml')
