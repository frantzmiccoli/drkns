from paver.easy import sh


import sys


def taest_list():
    _clean()
    output = _invoke_drkns('list')
    assert(len(output) > 6)
    assert('project1.run' in output)
    assert('project1.dependency1.hello' in output)


def test_run_partial():
    _clean()
    _invoke_drkns('run project1.run')

    ls_output = sh('ls /tmp', capture=True)

    assert('project1.out' in ls_output)
    assert('project2.out' not in ls_output)


def taest_run_complete():
    _clean()
    _invoke_drkns('run')

    ls_output = sh('ls /tmp', capture=True)

    assert('project1.out' in ls_output)
    assert('project2.out' in ls_output)


def _invoke_drkns(extra_args: str) -> str:
    command = '(export PYTHONPATH=${PYTHONPATH}:${PWD}/src;' \
              'cd testproject; python ../src/drkns/__init__.py ' \
              + extra_args + ')'
    output = sh(command, capture=True)
    return output


def _clean():
    command = 'rm -rf /tmp/*.out testproject/.drkns-persistence'
    sh(command)
