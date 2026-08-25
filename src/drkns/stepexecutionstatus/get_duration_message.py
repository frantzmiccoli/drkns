from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus

_slow_duration_threshold = 30


def get_duration_message(status: StepExecutionStatus) -> str:
    if (status.ignored) or (status.duration is None):
        return ''

    message = f' in {status.duration:.1f} s'

    if status.duration > _slow_duration_threshold:
        message += ' 🐢'

    return message
