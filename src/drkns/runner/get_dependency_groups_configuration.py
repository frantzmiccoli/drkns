from typing import List, Tuple


from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.exception import DependenciesNotAvailable
from drkns.runner.get_execution_plan import get_execution_plan


class _DependencyGroupsConfigurationResolver:

    def __init__(self, root_config_unit: ConfigUnit):
        self._root_config_unit: ConfigUnit = root_config_unit

        self._execution_plan_units: List[ConfigUnit] = []
        self._groups_configuration: \
            List[Tuple[str, List[ConfigUnit], List[str]]] = []
        self._available_dependencies: List[ConfigUnit] = []

    def get_groups_configuration(
            self
    ) -> List[Tuple[str, List[ConfigUnit], List[str]]]:
        self._load_execution_plan_units()
        self._resolve_group_configurations()

        return self._groups_configuration


    def _load_execution_plan_units(self):
        execution_plan = get_execution_plan(self._root_config_unit)

        for config_unit, _, _ in execution_plan:
            if config_unit in self._execution_plan_units:
                continue

            self._execution_plan_units.append(config_unit)

    def _resolve_group_configurations(self):
        while len(self._execution_plan_units) > 0:
            config_unit = self._execution_plan_units.pop(0)
            if not self._are_dependencies_available(config_unit):
                error_message = \
                    'This should never occur as we are proceeding through ' + \
                    'the ordered execution plan'

                raise DependenciesNotAvailable(error_message)

            group_name = config_unit.name
            group_units = [config_unit]
            self._available_dependencies.append(config_unit)
            dependency_groups_names = \
                [dependency.name
                 for dependency in config_unit.dependencies]
            group_configuration = \
                (group_name, group_units, dependency_groups_names)
            self._groups_configuration.append(
                group_configuration)

    def _are_dependencies_available(self, config_unit: ConfigUnit):
        for dependency in config_unit.dependencies:
            if dependency not in self._available_dependencies:
                return False

        return True


def get_dependency_groups_configuration(
        root_config: ConfigUnit
) -> List[Tuple[str, List[ConfigUnit], List[str]]]:
    resolver = _DependencyGroupsConfigurationResolver(root_config)
    return resolver.get_groups_configuration()
