import os

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.get_hash import get_hash


def get_unit_path(config_unit: ConfigUnit):
    persistence_directory = '.drkns-persistence'

    unit_directory = os.path.join(persistence_directory, config_unit.name)
    if not os.path.exists(unit_directory):
        os.makedirs(unit_directory, exist_ok=True)

    return os.path.join(unit_directory, get_hash(config_unit) + '.drknsdate')
