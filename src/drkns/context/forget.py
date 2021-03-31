from typing import Optional

import os
from shutil import rmtree

from drkns.context.get_unit_step_path import \
    _get_path_to_unit, persistence_directory


def forget(unit_name: Optional[str] = None):
    if unit_name is None:
        rmtree(persistence_directory)

    unit_path = _get_path_to_unit(unit_name)  # type: ignore
    if not os.path.exists(unit_path):
        return

    print(unit_path)
    rmtree(unit_path)
