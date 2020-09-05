from paver.easy import sh


def test_list():
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


def test_run_complete():
    _clean()
    _invoke_drkns('run')

    ls_output = sh('ls /tmp', capture=True)

    assert('project1.out' in ls_output)
    assert('project2.out' in ls_output)


def test_run_cache():
    _clean()
    _invoke_drkns('run')
    ls_output = sh('ls /tmp', capture=True)
    assert('project1.out' in ls_output)
    assert('project2.out' in ls_output)

    sh('rm /tmp/project*.out')

    _invoke_drkns('run')
    ls_output = sh('ls /tmp', capture=True)
    # the hash hasn't change the build should not have generated output
    assert('project1.out' not in ls_output)
    assert('project2.out' not in ls_output)

    project_file = 'testproject/project1/main.py'
    sh('echo "# for test" >> ' + project_file, capture=True)
    _invoke_drkns('run')
    ls_output = sh('ls /tmp', capture=True)
    assert('project1.out' in ls_output)
    assert('project2.out' not in ls_output)

    sh('cat ' + project_file + ' | grep -v test > ' + project_file + '.mod')
    sh('rm ' + project_file)
    sh('mv ' + project_file + '.mod ' + project_file)


def test_run_no_multi_dependencies_execution():
    _clean()
    _invoke_drkns('run')

    dependency_output_file = '/tmp/dependency1.out'
    line_count = 0
    with open(dependency_output_file, 'r') as f:
        for _ in f:
            line_count += 1

    assert(line_count == 1)


def _invoke_drkns(extra_args: str) -> str:
    command = '(export PYTHONPATH=${PYTHONPATH}:${PWD}/src;' \
              'cd testproject; python ../src/drkns/__init__.py ' \
              + extra_args + ')'
    output = sh(command, capture=True)
    return output


def _clean():
    command = 'rm -rf /tmp/*.out testproject/.drkns-persistence'
    sh(command)
