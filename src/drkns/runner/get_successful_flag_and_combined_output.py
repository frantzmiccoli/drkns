from typing import List, Tuple

from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus
from drkns.stepexecutionstatus.get_status_message_and_output_from_status import\
    get_status_message_and_output_from_status


def get_successful_flag_and_combined_output(
            execution_history: List[StepExecutionStatus],
            summary: bool = False,
            limit_output: bool = False
            ) -> Tuple[bool, List[str]]:
    outputs = []
    statuses = []
    successful = True
    for status in execution_history:
        message, output = get_status_message_and_output_from_status(status)

        statuses.append(message)

        if status.ignored or not status.successful:
            successful = False

        active_output = not status.ignored and not status.restored
        append_output = not limit_output or active_output
        if output is not None and append_output:
            outputs.append(output)

    if summary:
        return successful, statuses

    combined_output = []
    if len(outputs) > 0:
        combined_output += outputs + ['\n']

    combined_output += statuses

    return successful, combined_output
