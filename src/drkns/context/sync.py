from typing import Tuple


from drkns.context.get_unit_step_path import persistence_directory
from drkns.util import sh


def sync_in(target_s3_path: str) -> Tuple[int, str]:
    command = 'aws s3 sync {} {}'.format(target_s3_path, persistence_directory)
    status, output, _ = sh(command)
    return status, output


def sync_out(target_s3_path: str, delete: bool) -> Tuple[int, str]:
    delete_flag = ''
    if delete:
        delete_flag = '--delete'

    command = 'aws s3 sync {} {} {}'.format(
        persistence_directory, target_s3_path, delete_flag)

    status, output, _ = sh(command)
    return status, output
