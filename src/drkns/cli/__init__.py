import sys
from typing import Collection

from drkns.exception import MissingCommandException, UnknownCommandException
from drkns.loader.Loader import Loader
from drkns.runner.Runner import Runner
from drkns.config.ConfigUnit import ConfigUnit


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

        message = 'Unkown command: ' + command +\
                  '. Allowed commands are "run" and "check".'
        raise UnknownCommandException(message)

    def _check(self):
        config_unit = self._get_config_unit()
        error_string = config_unit.get_error_string()

        if error_string is None:
            sys.exit()

        sys.exit(error_string)

    def _run(self):
        config_unit = self._get_config_unit()
        runner = Runner()

        target = None
        if len(self._parsed_args) > 1:
            target = self._parsed_args[1]
        successful, output_lines = runner.run(config_unit, target)
        print('\n'.join(output_lines))
        if successful:
            sys.exit()

        sys.exit('An error occurred')

    def _list(self):
        config_unit = self._get_config_unit()
        steps = config_unit.get_steps()
        steps.reverse()
        print('\n'.join(steps))

    @staticmethod
    def _get_config_unit() -> ConfigUnit:
        loader = Loader()
        return loader.load('drkns.yml')
