from typing import Tuple, Optional

from drkns.exception import UnexpectedBranchException
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus
from drkns.util import BColors


def get_status_message_and_output_from_status(
    status: StepExecutionStatus
) -> Tuple[str, Optional[str]]:
    """

    :param status:
    :return: status_message and output (can be None)
    """
    output = None
    message = status.name() + ': ' + BColors.BOLD

    if status.hash is None:
        raise UnexpectedBranchException()

    if status.ignored:
        message += BColors.WARNING + f'Ignored @{status.hash}' + BColors.ENDC
    elif not status.successful:
        message += BColors.FAIL + f'Error @{status.hash}' + BColors.ENDC
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
