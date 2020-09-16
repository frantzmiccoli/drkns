import os

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.get_hash import get_hash

persistence_directory = '.drkns-persistence'
extension = '.drknsdata'


def get_unit_step_path(config_unit: ConfigUnit, step_name: str):
    unit_directory = os.path.join(
        persistence_directory, config_unit.name, step_name)
    if not os.path.exists(unit_directory):
        os.makedirs(unit_directory, exist_ok=True)

    return os.path.join(unit_directory, get_hash(config_unit) + extension)
