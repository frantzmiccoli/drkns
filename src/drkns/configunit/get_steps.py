from typing import List, Tuple, Optional

from drkns.configunit.ConfigUnit import ConfigUnit


def get_steps(start_config_unit: ConfigUnit, ignore_dependency: bool = False) \
        -> List[str]:
    """
    Return steps and dependency steps in proper execution order
    :param start_config_unit:
    :param ignore_dependency:
    :return:
    """
    steps: List[str] = []

    considered_prefixes_and_config_units: \
        List[Tuple[Optional[str], ConfigUnit]] = \
        [(None, start_config_unit)]

    while len(considered_prefixes_and_config_units) != 0:
        current_prefix, config_unit = \
            considered_prefixes_and_config_units.pop(0)

        for dependency_name in config_unit.dependencies.keys():
            if ignore_dependency:
                break

            prefix: str = dependency_name + '.'

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
