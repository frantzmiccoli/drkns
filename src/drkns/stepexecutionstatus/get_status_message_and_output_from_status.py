from typing import Tuple, Optional

from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus
from drkns.util import BColors


def get_status_message_and_output_from_status(status: StepExecutionStatus)\
        -> Tuple[str, Optional[str]]:
    """

    :param status:
    :return: status_message and output (can be None)
    """
    output = None
    message = status.name() + ': ' + BColors.BOLD
    if status.ignored:
        message += BColors.WARNING + 'Ignored' + BColors.ENDC
    elif not status.successful:
        message += BColors.FAIL + 'Error' + BColors.ENDC
    else:
        message += BColors.OKBLUE + 'OK' + BColors.ENDC

    if status.restored:
        message += ' (restored)'

    if not status.successful:
        output = 'Output for ' + status.name()

        if status.restored:
            output += ' (restored)'

        output += ': \n' + status.output + '\n--\n\n'

    return message, output
