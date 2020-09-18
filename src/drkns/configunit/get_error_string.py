import os
from typing import List, Optional

from drkns.configunit.ConfigUnit import ConfigUnit


def get_error_string(config_unit: ConfigUnit, indent: Optional[int] = None) \
        -> Optional[str]:
    if indent is None:
        indent = 0

    errors = _get_errors(config_unit, indent + 1)

    if len(errors) == 0:
        return None

    original_indent_string = '   ' * indent
    indent_string = '   ' * (indent + 1)
    return original_indent_string + 'Error in "' + config_unit.name + '":\n' +\
        indent_string + ('\n' + indent_string).join(errors) + '\n\n'


def _get_errors(config_unit: ConfigUnit, indent: int) -> List[str]:
    errors: List[str] = []
    if config_unit.directory is None:
        errors.append(config_unit.name + ': directory is not set')
    elif not os.path.exists(config_unit.directory):
        errors.append(config_unit.name + ': directory does not exist')
    if (len(config_unit.steps) == 0) and (len(config_unit.dependencies) == 0):
        message = config_unit.name + ': no steps nor dependencies are defined'
        errors.append(message)

    for name, dependency in config_unit.dependencies.items():
        dependency_error_string = get_error_string(dependency, indent)
        if dependency_error_string is not None:
            errors.append(dependency_error_string)

    return errors
