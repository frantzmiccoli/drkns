import yaml
import os

from drkns.loader.config.ConfigUnit import ConfigUnit
from drkns.loader.config import config_directory


class Loader:

    def __init__(self):
        pass

    def load(self, root_path, associated_name=None):
        root_path = os.path.abspath(root_path)
        if associated_name is None:
            associated_name = 'main'

        data = yaml.load(open(root_path), Loader=yaml.FullLoader)

        data.directory = data.get('directory', None)
        base_dir = os.path.dirname(root_path)
        if (data.directory is not None) and (not os.path.isabs(data.directory)):
            data.directory = os.path.join(base_dir, data.directory)

        for name, relative_path in data.get('dependencies', {}).items():
            target_path = os.path.abspath(os.path.join(base_dir, relative_path))
            if not (target_path in config_directory):
                dependency = self.load(target_path, name)
            else:
                dependency = config_directory[target_path]

            data['dependencies'][associated_name] = dependency

        config_unit = ConfigUnit(associated_name, data)
        config_directory[root_path] = config_unit
        return config_unit




