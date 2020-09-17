import sys
from typing import Collection
import os

from drkns.exception import MissingCommandException, UnknownCommandException,\
    MissingSyncDirectionException, MissingS3PathException
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.load import load
from drkns.configunit.run import run
from drkns.configunit.get_steps import get_steps
from drkns.configunit.get_error_string import get_error_string
from drkns.context.clean_persistence_files import clean_persistence_files
from drkns.context.sync import sync_in, sync_out


class Cli:

    def __init__(self):
        self._parsed_args: Collection[str] = []

    def handle(self):
        self._parsed_args = sys.argv[1:]
        if len(self._parsed_args) == 0:
            raise MissingCommandException()

        command = self._parsed_args[0]

        if command == 'check':
            self._check()
            return

        if command == 'list':
            self._list()
            return

        if command == 'sync':
            self._sync()
            return

        if command == 'run':
            self._run()
            return

        if command == 'clean':
            self._clean()
            return

        message = 'Unkown command: ' + command +\
                  '. Allowed commands are "run" and "check".'
        raise UnknownCommandException(message)

    def _check(self):
        config_unit = self._get_config_unit()
        error_string = get_error_string(config_unit)

        if error_string is None:
            sys.exit()

        sys.exit(error_string)

    def _list(self):
        config_unit = self._get_config_unit()
        steps = get_steps(config_unit)
        steps.reverse()
        print('\n'.join(steps))

    def _sync(self):
        if (len(self._parsed_args) < 2) \
                or (self._parsed_args[1] not in ['in', 'out']):
            message = 'Sync direction should be in or out'
            raise MissingSyncDirectionException(message)

        sync_direction = self._parsed_args[1]

        environment_variable_name = 'DRKNS_S3_PATH'
        target_s3_path = os.environ.get(environment_variable_name)
        if len(self._parsed_args) == 3:
            target_s3_path = self._parsed_args[2]

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
        if len(self._parsed_args) > 1:
            target = self._parsed_args[1]
        successful, output_lines = run(config_unit, target)
        if len(output_lines) > 0:
            print('\n'.join(output_lines))
        if successful:
            sys.exit()

        sys.exit(1)

    @staticmethod
    def _clean():
        clean_persistence_files()
        sys.exit()

    @staticmethod
    def _get_config_unit() -> ConfigUnit:
        return load('drkns.yml')
