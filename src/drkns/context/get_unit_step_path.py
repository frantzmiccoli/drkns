import os

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.get_hash import get_hash
from drkns.step.get_step_type import get_step_type

persistence_directory = '.drknspersistence'
extension = '.drknsdata'


def get_unit_step_path(config_unit: ConfigUnit, step_name: str):
    prefix = get_step_type(config_unit, step_name) + '_'

    unit_path = _get_path_to_unit(config_unit.name)
    unit_directory = os.path.join(unit_path, prefix + step_name)
    if not os.path.exists(unit_directory):
        os.makedirs(unit_directory, exist_ok=True)

    return os.path.join(unit_directory, get_hash(config_unit) + extension)


def _get_path_to_unit(unit_name: str) -> str:
    unit_name = unit_name.replace('/', '_')
    unit_name = unit_name.replace('..', '_')
    return os.path.join(persistence_directory, unit_name)
