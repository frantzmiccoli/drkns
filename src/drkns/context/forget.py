from typing import Optional

import os
import sys
from shutil import rmtree

from drkns.context.get_unit_step_path import \
    _get_path_to_unit, persistence_directory


_empty_warning_message = \
    'No files found to forget. You can use `drkns list` to see unit names'


def forget(unit_name: Optional[str] = None):
    clean_path = persistence_directory
    if unit_name is not None:
        clean_path = _get_path_to_unit(unit_name)  # type: ignore

    if not os.path.exists(clean_path):
        sys.stderr.write(_empty_warning_message)
        return

    # rmtree(clean_path)  # but aws s3 sync does not remove empty directories

    erased_something = False

    for root, dirs, files in os.walk(clean_path):
        for file in files:
            file_path = os.path.join(root, file)
            erased_something = True
            os.remove(file_path)

        if len(dirs) != 0:
            continue  # A marker will be in the root dirs

        with open(os.path.join(root, '.direxists'), 'a') as _:
            pass

    if not erased_something:
        sys.stderr.write(_empty_warning_message)
