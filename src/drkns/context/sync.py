from typing import Tuple


from drkns.context.get_unit_step_path import persistence_directory
from drkns.util import sh


def sync_in(target_s3_path: str) -> Tuple[int, str]:
    command = 'aws s3 sync {} {}'.format(target_s3_path, persistence_directory)
    return sh(command)


def sync_out(target_s3_path: str) -> Tuple[int, str]:
    command = 'aws s3 sync --delete {} {}'.format(persistence_directory, target_s3_path)
    return sh(command)

