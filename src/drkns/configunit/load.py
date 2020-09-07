import yaml
import os
from typing import Optional

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit import config_directory


def load(root_path: str, associated_name: Optional[str] = None)\
        -> ConfigUnit:
    root_path = os.path.abspath(root_path)
    if associated_name is None:
        associated_name = 'main'

    data = yaml.load(open(root_path), Loader=yaml.FullLoader)

    base_dir = os.path.dirname(root_path)
    data['directory'] = data.get('directory', '.')
    data['directory'] = os.path.join(base_dir, data['directory'])

    for name, relative_path in data.get('dependencies', {}).items():
        target_path = os.path.abspath(os.path.join(base_dir, relative_path))
        if not (target_path in config_directory):
            dependency = load(target_path, name)
        else:
            dependency = config_directory[target_path]

        data['dependencies'][name] = dependency

    config_unit = ConfigUnit(associated_name, data)
    config_directory[root_path] = config_unit
    return config_unit
