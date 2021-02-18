CHECK = 'check'
CLEANUP = 'cleanup'
BUILD = 'build'

types = [CHECK, CLEANUP, BUILD]


def check_step_type(step_type: str):
    if step_type in [CHECK, CLEANUP, BUILD]:
        return

    raise Exception('Unkown step_type: ' + step_type)
