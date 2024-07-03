from typing import Tuple, List, Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.exception import CircularDependencyException, \
    UnknownDependencyException
import drkns.step.step_type
from drkns.step.get_step_type import get_step_type
from drkns.runner.remove_execution_plan_redundancies \
    import remove_execution_plan_redundancies


def get_execution_plan(
    config_unit: ConfigUnit,
    step_name: Optional[str] = None
) -> List[Tuple[ConfigUnit, str, str]]:
    """
    Execution plan guarantees that steps are in dependency order:
    * Dependencies first
    * In order check steps, build steps and clean steps
    * If a specific steps is given, build steps not directly preceding it will
    be omitted

    :param config_unit:
    :param step_name:
    :return: config unit, step within the config unit, prefixed step name
    """
    # This public function only hide the parameters of the private one
    raw_execution_plan = _get_execution_plan(config_unit, step_name)
    execution_plan = remove_execution_plan_redundancies(raw_execution_plan)
    return execution_plan


def _get_execution_plan(
    config_unit: ConfigUnit,
    step_name: Optional[str] = None,
    allowed_types: Optional[List[str]] = None,
    prefix: Optional[str] = None
) -> List[Tuple[ConfigUnit, str, str]]:
    if step_name is None:
        prefix = '' if prefix is None else prefix
        steps = _get_nested_dependencies_steps(config_unit, prefix)

        steps += _get_internal_steps(config_unit, prefix,
            allowed_types=allowed_types)
        return steps

    nested_config_unit, final_step_name = \
        _get_nested_config_unit_and_step(config_unit, step_name)
    prefix_parts = step_name.split('.')
    if final_step_name is not None:  # The final part is a step
        prefix_parts.pop()
    step_type = None
    if final_step_name is not None:
        step_type = get_step_type(nested_config_unit, final_step_name)

    step_prefix = '.'.join(prefix_parts)
    step_prefix += '.' if step_prefix else ''

    no_dependencies_types =\
        [drkns.step.step_type.CHECK, drkns.step.step_type.CLEANUP]
    if step_type in no_dependencies_types:
        return _get_internal_steps(
            nested_config_unit, step_prefix, final_step_name)

    # we know step_type is BUILD or None
    steps = _get_nested_dependencies_steps(nested_config_unit, step_prefix,
                                           [drkns.step.step_type.CHECK])
    steps += _get_internal_steps(nested_config_unit, step_prefix,
                                 target_step_name=step_name)
    return steps


def _get_nested_dependencies_steps(
    config_unit: ConfigUnit,
    prefix: str,
    allowed_types: Optional[List[str]] = None
) -> List[Tuple[ConfigUnit, str, str]]:
    """
    If we are calling this function we want to resolve every dependency
    (at every steps i.e. check, build and cleanup)
    :param config_unit:
    :param prefix:
    :return:
    """
    # Circular dependency detection
    max_nesting = 10
    if prefix.count('.') > max_nesting:
        message = 'More than ' + str(max_nesting) +\
                  ' levels have been found, note that we do not support ' +\
                  'circular dependencies and believe that this is one instance.'
        raise CircularDependencyException(message)

    steps = []

    for dependency_unit in config_unit.dependencies:
        dependency_name = dependency_unit.name
        new_prefix = prefix + dependency_name + '.'
        steps += _get_execution_plan(
            dependency_unit, allowed_types=allowed_types, prefix=new_prefix)

    return steps


def _get_internal_steps(
    config_unit: ConfigUnit,
    prefix: str,
    target_step_name: Optional[str] = None,
    allowed_types: Optional[List[str]] = None
) -> List[Tuple[ConfigUnit, str, str]]:
    """

    :param config_unit:
    :param prefix:
    :param target_step_name: if specified will not include CHECK or BUILD steps
        after seeing this item
    :param allowed_types:
    :return:
    """
    step_names: List[str] = []

    allowed_types = drkns.step.step_type.types \
        if allowed_types is None else allowed_types

    has_check = drkns.step.step_type.CHECK in allowed_types
    has_build = drkns.step.step_type.BUILD in allowed_types

    if has_check or has_build:
        step_names += config_unit.get_steps(drkns.step.step_type.CHECK).keys()
    if has_build:
        step_names += config_unit.get_steps(drkns.step.step_type.BUILD).keys()

    # whatever happens we clean up
    step_names += config_unit.get_steps(drkns.step.step_type.CLEANUP).keys()

    plan_steps: List[Tuple[ConfigUnit, str, str]] = []
    found_target = False
    for step_name in step_names:
        is_cleanup = get_step_type(config_unit, step_name) == \
                     drkns.step.step_type.CLEANUP
        if found_target and not is_cleanup:
            continue

        prefixed_step_name = prefix if prefix is not None else ''
        prefixed_step_name += step_name
        plan_steps.append((config_unit, step_name, prefixed_step_name))
        if step_name == target_step_name:
            found_target = True

    return plan_steps


def _get_nested_config_unit_and_step(
    root_config_unit: ConfigUnit,
    composite_step_name: str
) -> Tuple[ConfigUnit, Optional[str]]:

    dot_index = composite_step_name.find('.')
    if dot_index == -1:
        dependency_config_unit = \
            root_config_unit.get_dependency(composite_step_name)
        if dependency_config_unit is not None:
            return dependency_config_unit, None
        return root_config_unit, composite_step_name

    dependency_name = composite_step_name[0:dot_index]
    dependency_config_unit = root_config_unit.get_dependency(dependency_name)
    if dependency_config_unit is None:
        message = dependency_name + ' is not a dependency in ' + \
                  root_config_unit.name
        raise UnknownDependencyException(message)

    sub_step_name = composite_step_name[dot_index + 1:]
    return _get_nested_config_unit_and_step(dependency_config_unit,
                                            sub_step_name)
