from dirhash import dirhash  # type: ignore
from hashlib import sha1

from drkns.configunit.ConfigUnit import ConfigUnit


def get_hash(config_unit: ConfigUnit) -> str:
    if config_unit.hash is None:
        config_unit.hash = _get_computed_hash(config_unit)

    return config_unit.hash


def _get_computed_hash(config_unit: ConfigUnit) -> str:
    hash_input = \
        dirhash(config_unit.directory, 'sha1',
                ignore=config_unit.ignored)

    for dependency_config_unit in config_unit.dependencies:
        hash_input += _get_computed_hash(dependency_config_unit)

    hashed = hash_input[0:7] + '-' + \
        sha1(hash_input.encode('utf-8')).hexdigest()
    return hashed
