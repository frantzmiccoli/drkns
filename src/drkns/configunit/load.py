import yaml
import os
import re
from typing import Optional, List

from drkns.exception import MalformedIgnorePatternException
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit import config_directory

_ignored_by_default = [
    '.git', '.git/', '.drknspersistence/', '*.pyc', '__pycache__/'
]


def load(
        root_path: str,
        associated_name: Optional[str] = None,
        inherited_ignored: Optional[List[str]] = None
        ) -> ConfigUnit:
    root_path = os.path.abspath(root_path)
    if associated_name is None:
        associated_name = 'main'

    if inherited_ignored is None:
        inherited_ignored = []

    if os.path.isdir(root_path):
        root_path = os.path.join(root_path, 'drkns.yml')

    data = yaml.load(open(root_path), Loader=yaml.FullLoader)

    base_dir = os.path.dirname(root_path)
    if 'directory' in data:
        data['directory'] = \
            os.path.abspath(os.path.join(base_dir, data['directory']))
    else:
        data['directory'] = base_dir

    config_unit_ignored = _get_ignored(root_path)
    parsed_ignored = inherited_ignored + config_unit_ignored

    for name, relative_path in data.get('dependencies', {}).items():
        target_path = os.path.abspath(os.path.join(base_dir, relative_path))
        if not (target_path in config_directory):
            dependency = load(target_path, name, parsed_ignored)
        else:
            dependency = config_directory[target_path]

        data['dependencies'][name] = dependency

    ignored = parsed_ignored + _ignored_by_default
    config_unit = ConfigUnit(associated_name, data, ignored)

    config_directory[root_path] = config_unit

    return config_unit


def _get_ignored(path: str) -> List[str]:
    dir_name = path
    if not os.path.isdir(dir_name):
        dir_name = os.path.dirname(dir_name)

    drkns_ignore_path = os.path.join(dir_name, '.drknsignore')
    if not os.path.exists(drkns_ignore_path):
        return []

    handle = open(drkns_ignore_path)
    ignored_raw = handle.read()
    ignored_raw = ignored_raw.replace('\r', ' ')
    ignored_raw = ignored_raw.replace('\n', ' ')
    ignored_raw = ignored_raw.replace(',', ' ')
    separator = u' '
    ignored_raw = re.sub(r'\s\s+', separator, ignored_raw)

    ignored = ignored_raw.split(separator)
    _check_ignored(ignored)

    return ignored


def _check_ignored(ignored: List[str]):
    for ignored_item in ignored:
        slash_index = ignored_item.find('/')
        if slash_index == -1:
            continue
        if slash_index == len(ignored_item) -1:
            continue

        error_message = '"/" is only allowed at the end of a pattern, found "' \
                        + ignored_item + '"'
        MalformedIgnorePatternException(
            error_message)