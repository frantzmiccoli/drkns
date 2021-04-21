from paver.easy import sh

from drkns.configunit import ConfigUnit


def invoke_drkns(project: str, extra_args: str) -> str:
    project_depth = project.count('/')
    command = '(export PYTHONPATH=${PYTHONPATH}:${PWD}/src;' \
              'cd testprojects/' + project + \
              '; python ' + ('../' * project_depth) +\
              '../../src/drkns/__init__.py ' +\
              extra_args + ')'
    output = sh(command, capture=True)
    return output


def clean():
    command = 'rm -rf /tmp/*.drknsdemo.out testprojects/*/.drknspersistence ' \
              'testprojects/*/*/.drknspersistence'
    sh(command)


def get_mock_config_unit() -> ConfigUnit:

    sub_dependency_1_config_unit = ConfigUnit('sub_dependency_1', {
        'checkSteps': {'sub_dependency_1_check_step_1': 'ls'},
        'buildSteps': {'sub_dependency_1_build_step_1': 'ls'},
        'cleanupSteps': {'sub_dependency_1_cleanup_step_1': 'ls'},
    }, [])

    dependency_1_config_unit = ConfigUnit('dependency_1', {
        'checkSteps': {'dependency_1_check_step_1': 'ls'},
        'buildSteps': {'dependency_1_build_step_1': 'ls'},
        'cleanupSteps': {'dependency_1_cleanup_step_1': 'ls'},
        'dependencies': [sub_dependency_1_config_unit]
    }, [])

    dependency_2_config_unit = ConfigUnit('dependency_2', {
        'checkSteps': {'dependency_2_check_step_1': 'ls'},
        'buildSteps': {'dependency_2_build_step_1': 'ls'},
        'cleanupSteps': {'dependency_2_cleanup_step_1': 'ls'},
    }, [])

    root_config_unit = ConfigUnit('root', {
        'checkSteps': {'root_check_step_1': 'ls'},
        'buildSteps': {'root_build_step_1': 'ls'},
        'cleanupSteps': {'root_cleanup_step_1': 'ls'},
        'dependencies': [
            dependency_1_config_unit,
            dependency_2_config_unit
        ]
    }, [])

    return root_config_unit
