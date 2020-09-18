import subprocess
import sys
from typing import Tuple, Optional


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


def sh(command: str, detached: Optional[bool] = None) -> Tuple[int, str]:
    kwargs = {
        'shell': True,
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.STDOUT
    }

    p = subprocess.Popen(command, **kwargs)  # type: ignore

    if detached:
        return 0, 'Detached process'

    p_stdout = p.communicate()[0]
    if p_stdout is not None:
        p_stdout = p_stdout.decode(sys.getdefaultencoding(), 'ignore')

    return p.returncode, p_stdout
