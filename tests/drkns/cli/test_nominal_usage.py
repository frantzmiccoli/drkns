from paver.easy import sh
import time
from tests.drkns.util import clean, invoke_drkns


def test_check():
    clean()
    output = invoke_drkns('nominalcase', 'check')
    assert (len(output) == 0)


def test_list():
    clean()
    output = invoke_drkns('nominalcase', 'list')
    assert(len(output) > 6)
    assert('project1.run' in output)
    assert('project1.dependency1.hello' in output)
    assert('project2.dependency1WithAnotherKey.run' not in output)


def test_debug():
    clean()
    output = invoke_drkns('nominalcase', 'debug')
    assert(len(output) > 6)


def test_run_partial():
    clean()
    invoke_drkns('nominalcase', 'run project1.run')

    ls_output = sh('ls /tmp', capture=True)

    assert('project1.drknsdemo.out' in ls_output)
    assert('project2.drknsdemo.out' not in ls_output)

    clean()
    invoke_drkns('nominalcase', 'run project1')

    ls_output = sh('ls /tmp', capture=True)

    assert ('project1.drknsdemo.out' in ls_output)


def test_run_complete():
    clean()
    t0 = time.time()
    drkns_output = invoke_drkns('nominalcase', 'run')

    ls_output = sh('ls /tmp', capture=True)

    t1 = time.time()
    execution_time = t1 - t0
    assert(execution_time < 10)

    assert('dummyCleanup' in drkns_output)

    assert('project1.drknsdemo.out' in ls_output)
    assert('project2.drknsdemo.out' in ls_output)
    assert('project2built.drknsdemo.out' in ls_output)


def test_run_cache():
    clean()
    invoke_drkns('nominalcase', 'run')
    ls_output = sh('ls /tmp', capture=True)
    assert('project1.drknsdemo.out' in ls_output)
    assert('project2.drknsdemo.out' in ls_output)

    sh('rm /tmp/project*.out')

    invoke_drkns('nominalcase', 'run')
    ls_output = sh('ls /tmp', capture=True)
    # the hash hasn't changed the build should not have generated output
    assert('project1.drknsdemo.out' not in ls_output)
    assert('project2.drknsdemo.out' not in ls_output)

    project_file = 'testprojects/nominalcase/project1/main.py'
    sh('echo "# for test" >> ' + project_file, capture=True)
    invoke_drkns('nominalcase', 'run')
    ls_output = sh('ls /tmp', capture=True)
    assert('project1.drknsdemo.out' in ls_output)
    assert('project2.drknsdemo.out' not in ls_output)

    sh('cat ' + project_file + ' | grep -v test > ' + project_file + '.mod')
    sh('rm ' + project_file)
    sh('mv ' + project_file + '.mod ' + project_file)

    ignored_file = 'testprojects/nominalcase/project1/main.py.tmp'
    sh('rm -rf /tmp/project*.drknsdemo.out', capture=True)
    sh('echo "something that should not trigger a build" >> ' + ignored_file)
    invoke_drkns('nominalcase', 'run')
    ls_output = sh('ls /tmp', capture=True)
    assert('project1.drknsdemo.out' not in ls_output)
    assert('project2.drknsdemo.out' not in ls_output)
    sh('rm ' + ignored_file)

    invoke_drkns('nominalcase', 'forget project1')
    invoke_drkns('nominalcase', 'run')
    ls_output = sh('ls /tmp', capture=True)
    assert ('project1.drknsdemo.out' in ls_output)


def test_run_no_multi_dependencies_execution():
    clean()
    invoke_drkns('nominalcase', 'run')

    dependency_output_file = '/tmp/dependency1.drknsdemo.out'
    line_count = 0
    with open(dependency_output_file, 'r') as f:
        for _ in f:
            line_count += 1

    assert(line_count == 1)
