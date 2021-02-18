import copy
from typing import Tuple, List, Dict, Optional


from drkns.util import sh
from drkns.configunit import ConfigUnit
from drkns.stepexecutionstatus.StepExecutionStatus import StepExecutionStatus

from drkns.step.get_step_type import get_step_type
import drkns.step.step_type
from drkns.context.get_past_execution_status import \
    get_past_execution_status
from drkns.context.store_past_execution_status import \
    store_past_execution_status


def run_plan(plan: List[Tuple[ConfigUnit, str, str]]) \
        -> List[StepExecutionStatus]:
    return _PlanRunner(plan).run()


class _PlanRunner:

    def __init__(self, plan: List[Tuple[ConfigUnit, str, str]]):
        self._plan: List[Tuple[ConfigUnit, str, str]] = plan
        self._status_history: List[StepExecutionStatus] = []
        self._failed_dependency_check_statuses: Dict[str, StepExecutionStatus] = {}
        self._failed_dependency_build_statuses: Dict[str, StepExecutionStatus] = {}
        self._processing_config_unit: Optional[ConfigUnit] = None

    def run(self) -> List[StepExecutionStatus]:
        self._status_history = []
        for config_unit, step_name, prefixed_step_name in self._plan:
            self._clean_up_pending_processes_if_needed(config_unit)
            step_execution_status = \
                self._get_execution_status_from_past_execution(
                    config_unit, step_name)

            if step_execution_status is None:
                step_execution_status = self._run(config_unit, step_name)

            self._handle_execution_status(config_unit, step_execution_status)

        self._clean_up_pending_processes_if_needed()

        return self._status_history

    # BEGIN cleanup: Remove pending processes than can be spawned by steps when
    # they are not needed anymore

    def _clean_up_pending_processes_if_needed(
        self,
        current_config_unit: ConfigUnit = None
    ):
        need_process_cleanup = self._need_to_cleanup_pending_processes(
            current_config_unit)

        to_cleanup_config_unit = self._processing_config_unit
        self._processing_config_unit = current_config_unit
        if (not need_process_cleanup) or (to_cleanup_config_unit is None):
            # `to_cleanup_config_unit` is None is here to silence mypy, it's
            # already checked in need_process_cleanup
            return

        while len(to_cleanup_config_unit.pending_subprocesses) != 0:
            subprocess = to_cleanup_config_unit.pending_subprocesses.pop(0)
            subprocess.terminate()

    def _need_to_cleanup_pending_processes(
            self,
            current_config_unit: Optional[ConfigUnit]
            ) -> bool:
        if self._processing_config_unit is None:
            return False

        if current_config_unit is None:
            return True

        new_config_unit = current_config_unit.name != \
            self._processing_config_unit.name
        return new_config_unit

    # END cleanup

    # noinspection PyMethodMayBeStatic
    def _run(self, config_unit: ConfigUnit, step_name: str) \
            -> StepExecutionStatus:
        """
        Actually calls the underlying command

        :param config_unit:
        :param step_name:
        :return:
        """
        step_type = get_step_type(config_unit, step_name)
        step = config_unit.get_steps(step_type)[step_name]

        # Run command
        command = '(cd "' + config_unit.directory + '"; \n' + step.command +\
                  '\n)'
        return_code, output, subprocess = sh(command, detached=step.background)
        successful = return_code == 0

        if subprocess.poll() is None:
            config_unit.pending_subprocesses.append(subprocess)

        step_execution_status = \
            StepExecutionStatus(config_unit.name, step_name,
                                successful=successful, output=output,
                                step_type=step_type)

        return step_execution_status

    def _handle_execution_status(
            self,
            config_unit: ConfigUnit,
            step_execution_status: StepExecutionStatus):

        step_type = step_execution_status.step_type
        is_check = step_type == drkns.step.step_type.CHECK
        successful = step_execution_status.successful
        if (not successful) and is_check:
            self._failed_dependency_check_statuses[config_unit.name] = \
                step_execution_status

        is_build = step_type == drkns.step.step_type.BUILD
        if (not successful) and is_build:
            self._failed_dependency_build_statuses[config_unit.name] = \
                step_execution_status

        if not step_execution_status.restored:
            store_past_execution_status(config_unit, step_execution_status)

        self._status_history.append(step_execution_status)

    # BEGIN past status retrieval:
    #   - Either from a previous execution without dependent code change
    #   - Either from a step that failed on which this step depends

    def _get_execution_status_from_past_execution(
            self,
            config_unit: ConfigUnit,
            step_name: str
            ) -> Optional[StepExecutionStatus]:
        """
        Will resolve a persisted execution status or a failed one from
        dependency execution
        :param config_unit:
        :param step_name:
        :return:
        """
        execution_status = get_past_execution_status(config_unit, step_name)
        if execution_status is not None:
            return copy.deepcopy(execution_status)

        return self._get_cascaded_failure_execution_status(
            config_unit, step_name)

    def _get_cascaded_failure_execution_status(
            self,
            config_unit: ConfigUnit,
            step_name: str
            ) -> Optional[StepExecutionStatus]:
        blocking_execution_status = \
            self._get_blocking_failure_execution_status(config_unit, step_name)

        if blocking_execution_status is None:
            return None

        output = 'Previous failure of ' \
                 + blocking_execution_status.config_unit_name + ' / ' + \
                 blocking_execution_status.step_name

        if blocking_execution_status.restored:
            output += ' (restored)'

        return StepExecutionStatus(
            config_unit.name,
            step_name,
            ignored=True,
            successful=False,
            step_type=blocking_execution_status.step_type,
            output=output)

    def _get_blocking_failure_execution_status(
            self,
            config_unit: ConfigUnit,
            step_name: str
            ) -> Optional[StepExecutionStatus]:
        step_type = get_step_type(config_unit, step_name)

        if step_type == drkns.step.step_type.CLEANUP:
            return None

        if config_unit.name in self._failed_dependency_check_statuses:
            return self._failed_dependency_check_statuses[config_unit.name]

        if step_type == drkns.step.step_type.CHECK:
            return None

        # we are sure it is a "build" step now

        if config_unit.name in self._failed_dependency_build_statuses:
            return self._failed_dependency_build_statuses[config_unit.name]

        for dependency_name, _ in config_unit.dependencies.items():
            if dependency_name in self._failed_dependency_check_statuses:
                return self._failed_dependency_check_statuses[dependency_name]

        return None

    # END past status retrieval
