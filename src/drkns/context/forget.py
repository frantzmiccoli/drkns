from typing import Optional, Tuple

import os
import sys
from shutil import rmtree

from drkns.context.get_unit_step_path import \
    _get_path_to_unit, persistence_directory


_to_short_extra_pattern_error_message = \
    'Extra pattern is too short'

_empty_warning_message = \
    'No files found to forget. You can use `drkns list` to see unit names.'


def forget(unit_and_pattern_input: str):
    unit_name, extra_pattern = \
        _get_unit_name_and_extra_pattern(unit_and_pattern_input)

    clean_path = _get_path_to_unit(unit_name)

    if not os.path.exists(clean_path):
        sys.stderr.write(_empty_warning_message)
        return

    # rmtree(clean_path)  # but aws s3 sync does not remove empty directories
    erased_something = False
    for root, dirs, files in os.walk(clean_path):
        for file in files:
            if not file.startswith(extra_pattern):
                continue

            file_path = os.path.join(root, file)
            erased_something = True
            os.remove(file_path)

        if len(dirs) != 0:
            continue  # A marker will be in the root dirs

        with open(os.path.join(root, '.direxists'), 'a') as _:
            pass

    if not erased_something:
        sys.stderr.write(_empty_warning_message)


def _get_unit_name_and_extra_pattern(
    unit_and_pattern_input: str
) -> Tuple[str, str]:
    parts = unit_and_pattern_input.split('/')

    # similar substitution when generating paths
    unit_name = parts.pop(0).replace('.', '_')

    extra_pattern = parts.pop(0) if len(parts) > 0 else ''
    if (len(extra_pattern) > 0) and (len(extra_pattern) < 12):
        sys.stderr.write(_to_short_extra_pattern_error_message)
        sys.exit(1)

    return unit_name, extra_pattern
