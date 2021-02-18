from tests.drkns.util import get_mock_config_unit

from drkns.runner.get_execution_plan import get_execution_plan
from drkns.exception import CircularDependencyException


def test_get_execution_plan_nominal_case():
    mock_config_unit = get_mock_config_unit()
    execution_plan = get_execution_plan(mock_config_unit)
    prefixed_names = [prefixed_name for _, _, prefixed_name in execution_plan]

    assert('dependency_1.sub_dependency_1.sub_dependency_1_check_step_1'
           in prefixed_names)
    assert('dependency_1.dependency_1_check_step_1' in prefixed_names)
    assert('root_check_step_1' in prefixed_names)

    # All checks should be performed before build
    assert(prefixed_names.index('root_build_step_1') >
           prefixed_names.index('dependency_1.dependency_1_check_step_1'))
    assert (prefixed_names.index('dependency_1.dependency_1_check_step_1') >
            prefixed_names.index(
                'dependency_1.sub_dependency_1.sub_dependency_1_check_step_1'))


def test_get_execution_plan_target_step_case():
    mock_config_unit = get_mock_config_unit()
    step_name = 'dependency_2.dependency_2_build_step_1'
    execution_plan = get_execution_plan(mock_config_unit, step_name)
    prefixed_names = [prefixed_name for _, _, prefixed_name in execution_plan]

    assert('dependency_1.sub_dependency_1.sub_dependency_1_check_step_1'
            not in prefixed_names)
    assert('dependency_1.dependency_1_check_step_1' not in prefixed_names)
    assert('root_check_step_1' not in prefixed_names)

    assert('dependency_2.dependency_2_check_step_1' in prefixed_names)
    assert('dependency_2.dependency_2_build_step_1' in prefixed_names)
    # clean up no matter what
    assert('dependency_2.dependency_2_cleanup_step_1' in prefixed_names)

    step_name = 'dependency_1.dependency_1_check_step_1'
    execution_plan = get_execution_plan(mock_config_unit, step_name)
    prefixed_names = [prefixed_name for _, _, prefixed_name in execution_plan]

    assert('dependency_1.sub_dependency_1.sub_dependency_1_check_step_1'
           not in prefixed_names) # check do not trigger dependencies
    assert('dependency_1.dependency_1_check_step_1' in prefixed_names)
    assert('dependency_1.dependency_1_cleanup_step_1' in prefixed_names)

    step_name = 'dependency_1.dependency_1_build_step_1'
    execution_plan = get_execution_plan(mock_config_unit, step_name)
    prefixed_names = [prefixed_name for _, _, prefixed_name in execution_plan]

    assert('dependency_1.sub_dependency_1.sub_dependency_1_check_step_1'
           in prefixed_names)  # build do trigger dependencies


def test_get_execution_plan_target_dependency_case():
    mock_config_unit = get_mock_config_unit()
    step_name = 'dependency_2'
    execution_plan = get_execution_plan(mock_config_unit, step_name)
    prefixed_names = [prefixed_name for _, _, prefixed_name in execution_plan]

    assert('dependency_2.dependency_2_check_step_1' in prefixed_names)
    assert('dependency_1.dependency_1_check_step_1' not in prefixed_names)
    assert('root_check_step_1' not in prefixed_names)


def test_get_execution_plan_loop_should_be_detected():
    mock_config_unit = get_mock_config_unit()
    mock_config_unit.dependencies['dependency_1'].dependencies['root'] = \
        mock_config_unit

    exception_count = 0
    try:
        get_execution_plan(mock_config_unit)
    except CircularDependencyException:
        exception_count += 1

    assert(exception_count == 1)
