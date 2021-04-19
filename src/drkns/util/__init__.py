from subprocess import Popen, PIPE, STDOUT
import sys
from typing import Tuple, Optional, List


class BColors:

    # source: https://stackoverflow.com/questions/287871
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def sh(command: str, detached: Optional[bool] = None)\
        -> Tuple[int, str, Popen]:
    kwargs = {
        'shell': True,
        'stdin': PIPE,
        'stdout': PIPE,
        'stderr': STDOUT
    }

    p = Popen(command, **kwargs)  # type: ignore

    if detached:
        return 0, 'Detached process', p

    p_stdout = p.communicate()[0]
    if p_stdout is not None:
        p_stdout = p_stdout.decode(sys.getdefaultencoding(), 'ignore')

    return p.returncode, p_stdout, p


def get_longest_common_prefix(items: List[str]) -> str:
    longest_prefix = ''
    if len(items) == 0:
        return longest_prefix

    max_index = min([len(item) for item in items])
    for i in range(0, max_index):
        reference_char = items[0][i]
        for item in items:
            if item[i] != reference_char:
                return longest_prefix

        longest_prefix += reference_char

    return longest_prefix
