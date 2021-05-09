from typing import Optional

import os
from shutil import rmtree

from drkns.context.get_unit_step_path import \
    _get_path_to_unit, persistence_directory


def forget(unit_name: Optional[str] = None):
    clean_path = persistence_directory
    if unit_name is not None:
        clean_path = _get_path_to_unit(unit_name)  # type: ignore

    if not os.path.exists(clean_path):
        return

    # rmtree(clean_path)  # but aws s3 sync does not remove empty directories

    for root, dirs, files in os.walk(clean_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

        if len(dirs) != 0:
            continue  # A marker will be in the root dirs

        with open(os.path.join(root, '.direxists'), 'a') as _:
            pass
