import os
from typing import List, Optional

from drkns.configunit.ConfigUnit import ConfigUnit
import drkns.step.step_type


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

    has_steps = (len(config_unit.check_steps) != 0) or \
                (len(config_unit.build_steps) != 0)
    has_dependencies = len(config_unit.dependencies) != 0
    if (not has_steps) and (not has_dependencies):
        message = config_unit.name + ': no steps nor dependencies are defined'
        errors.append(message)

    for dependency in config_unit.dependencies:
        dependency_error_string = get_error_string(dependency, indent)
        if dependency_error_string is not None:
            errors.append(dependency_error_string)

    names_error = _get_dependency_or_step_names_error(config_unit)
    if names_error is not None:
        errors.append(names_error)

    return errors


def _get_dependency_or_step_names_error(
        config_unit: ConfigUnit) -> Optional[str]:
    names = [dependency.name for dependency in config_unit.dependencies]
    for step_type in drkns.step.step_type.types:
        names += list(config_unit.get_steps(step_type).keys())

    duplicate_names = set()
    unique_names = set()
    for step_name in names:
        if step_name in duplicate_names:
            continue

        if step_name in unique_names:
            duplicate_names.add(step_name)
            continue

        unique_names.add(step_name)

    if len(duplicate_names) == 0:
        return None

    message = 'Config unit ' + config_unit.name + \
              ' reuses step or dependency names: ' \
              + ', '.join(duplicate_names)  # type: ignore
    return message
