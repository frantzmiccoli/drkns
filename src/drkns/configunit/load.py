from ruamel.yaml import YAML

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
        inherited_ignored: Optional[List[str]] = None,
        original_root_path: Optional[str] = None
        ) -> ConfigUnit:
    root_path = os.path.abspath(root_path)
    if original_root_path is None:
        original_root_path = os.path.abspath(root_path)

    if not os.path.isdir(original_root_path):
        original_root_path = os.path.dirname(original_root_path)

    if inherited_ignored is None:
        inherited_ignored = []

    unit_name = _get_unit_name(root_path, original_root_path)

    if os.path.isdir(root_path):
        root_path = os.path.join(root_path, 'drkns.yml')

    with open(root_path) as handle:
        yaml = YAML(typ='safe')
        data = yaml.load(handle)

    base_dir = os.path.dirname(root_path)
    if 'directory' in data:
        data['directory'] = \
            os.path.abspath(os.path.join(base_dir, data['directory']))
    else:
        data['directory'] = base_dir

    config_unit_ignored = _get_ignored(root_path)
    parsed_ignored = inherited_ignored + config_unit_ignored

    raw_dependencies = data.get('dependencies', [])

    if isinstance(raw_dependencies, dict):
        error_message = 'dependencies must be an array of path now, ' + \
                        'error in: ' + root_path
        raise Exception(error_message)

    parsed_dependencies = []
    for relative_path in raw_dependencies:
        target_path = os.path.abspath(os.path.join(base_dir, relative_path))
        if not (target_path in config_directory):
            dependency = load(target_path, parsed_ignored, original_root_path)
        else:
            dependency = config_directory[target_path]

        parsed_dependencies.append(dependency)

    data['dependencies'] = parsed_dependencies

    ignored = parsed_ignored + _ignored_by_default
    config_unit = ConfigUnit(unit_name, data, ignored)

    config_directory[root_path] = config_unit

    return config_unit


def _get_unit_name(config_path: str, original_root_path: str) -> str:
    if not os.path.isdir(config_path):
        config_path = os.path.dirname(config_path)

    if config_path == original_root_path:
        return 'main'

    unit_name = \
        os.path.relpath(config_path, original_root_path)

    unit_name = unit_name.replace('/', '_')
    unit_name = unit_name.replace('.', '_')

    if unit_name == '_':
        import sys
        sys.exit()

    return unit_name


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