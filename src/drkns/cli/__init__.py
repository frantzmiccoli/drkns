import sys
from typing import Collection

from drkns.exception import MissingCommandException, UnknownCommandException
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.load import load
from drkns.configunit.run import run
from drkns.configunit.get_steps import get_steps
from drkns.configunit.get_error_string import get_error_string
from drkns.context.clean_persistence_files import clean_persistence_files


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

        if command == 'run':
            self._run()
            return

        if command == 'list':
            self._list()
            return

        if command == 'clean':
            clean_persistence_files()
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

    def _list(self):
        config_unit = self._get_config_unit()
        steps = get_steps(config_unit)
        steps.reverse()
        print('\n'.join(steps))

    @staticmethod
    def _get_config_unit() -> ConfigUnit:
        return load('drkns.yml')
