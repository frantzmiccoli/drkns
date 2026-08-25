from drkns.exception import UnexpectedBranchException

CHECK = 'check'
CLEANUP = 'cleanup'
BUILD = 'build'

types = [CHECK, CLEANUP, BUILD]


def check_step_type(step_type: str):
    if step_type in [CHECK, CLEANUP, BUILD]:
        return

    raise UnexpectedBranchException('Unkown step_type: ' + step_type)
