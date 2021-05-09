from os import walk, path, unlink
import pickle
import datetime

from drkns.context.get_unit_step_path import persistence_directory, extension
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus


def clean_persistence_files():
    if not path.exists(persistence_directory):
        return

    too_old_file_paths = _get_too_old_file_paths()

    for too_old_file_path in too_old_file_paths:
        unlink(too_old_file_path)


def _get_too_old_file_paths():
    if not path.exists(persistence_directory):
        return

    too_old_paths = []

    for (dir_path, _, filenames) in walk(persistence_directory):
        if len(filenames) < 3:  # This step is not executed very often
            continue

        for filename in filenames:
            if path.splitext(filename)[-1] != extension:
                continue

            file_path = path.join(dir_path, filename)

            if _is_file_to_old(file_path):
                too_old_paths.append(file_path)

    return too_old_paths


def _is_file_to_old(file_path) -> bool:
    status = _get_persisted_status(file_path)
    four_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=4)
    return status.datetime < four_weeks_ago


def _get_persisted_status(file_path) -> StepExecutionStatus:
    with open(file_path, 'rb') as persisted_file:
        status = pickle.load(persisted_file)
        return status
