from paver.easy import sh
import time
from tests.util import clean, invoke_drkns


def test_simple_broken_build():
    clean()
    initial_output = invoke_drkns('failingdependenciescase/project1',
                          'run --force-success')

    ls_output = sh('ls /tmp', capture=True)
    assert('dependency1.neverranbuild.drknsdemo.out' not in ls_output)
    assert('dependency1.cleanup.drknsdemo.out' in ls_output)
    assert('project1.check.drknsdemo.out' in ls_output)
    assert('project1.failedbuildbecausedep1failed.drknsdemo.out'
           not in ls_output)
    assert ('project1.cleanup.drknsdemo.out' in ls_output)

    invoke_drkns('failingdependenciescase/project1',
                 'run --force-success')
    ls_output = sh('ls /tmp', capture=True)
    # previously observed bug
    assert('dependency1.neverranbuild.drknsdemo.out' not in ls_output)

    limited_output = invoke_drkns('failingdependenciescase/project1',
                                  'run --force-success --limit-output')
    assert (len(limited_output) < len(initial_output))

    summary_output = invoke_drkns('failingdependenciescase/project1',
                                  'run --force-success --summary')
    assert(len(summary_output) < len(initial_output))


def test_broken_full_build():
    """
    The full build should fail, and thus the build steps of the main element
    should never be run, but the check steps should be ran.
    :return:
    """
    clean()
    output = invoke_drkns('failingdependenciescase', 'run --force-success')

    ls_output = sh('ls /tmp', capture=True)
    assert('main.neverRanBuildStep1.drknsdemo.out' not in ls_output)
    assert('main.neverRanBuildStep2.drknsdemo.out' not in ls_output)
    assert('main.checkStep1.drknsdemo.out' in ls_output)
    assert('dependency1.neverranbuild.drknsdemo.out' not in ls_output)
    assert('dependency1.cleanup.drknsdemo.out' in ls_output)
    assert('project1.check.drknsdemo.out' in ls_output)
    assert('project1.failedbuildbecausedep1failed.drknsdemo.out'
            not in ls_output)


def test_working_project_build():
    """
    Project 2 and project 3 have no failing dependencies.
    They should build without problems.
    Project 3 check step have an error but it should not prevent the execution
    of the other cleanup step
    :return:
    """
    clean()
    invoke_drkns('failingdependenciescase', 'run --force-success')

    ls_output = sh('ls /tmp', capture=True)
    assert('project2.check.drknsdemo.out' in ls_output)
    assert('project2.built.drknsdemo.out' in ls_output)
    assert('project2.built.drknsdemo.out' in ls_output)
    assert('project3.succesbecausedep2failedatbuild.drknsdemo.out'
           in ls_output)
    assert('project3.cleanup1.drknsdemo.out' not in ls_output)
    assert('project3.cleanup2.drknsdemo.out' in ls_output)
