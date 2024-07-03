from typing import Tuple


from drkns.context.get_unit_step_path import persistence_directory
from drkns.util import sh


def sync_in(target_s3_path: str) -> Tuple[int, str]:
    _configure_s3_if_needed()
    command = 'aws s3 sync {} {}'.format(target_s3_path, persistence_directory)
    status, output, _ = sh(command)
    return status, output


def sync_out(target_s3_path: str, delete: bool) -> Tuple[int, str]:
    _configure_s3_if_needed()
    delete_flag = ''
    if delete:
        delete_flag = '--delete'

    command = 'aws s3 sync {} {} {}'.format(
        persistence_directory, target_s3_path, delete_flag)

    status, output, _ = sh(command)
    return status, output


def _configure_s3_if_needed() -> bool:
    status, _, _ = \
        sh('aws configure get default.s3.max_concurrent_requests')
    if status == 0:
        # A value has been defined, we do not play with it
        return False

    command = """
        aws configure set default.s3.max_concurrent_requests 400
        aws configure set default.s3.max_queue_size 10000
        aws configure set default.s3.multipart_threshold 4MB
        aws configure set default.s3.multipart_chunksize 4MB
    """
    sh(command)

    return status == 0
