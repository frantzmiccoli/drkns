from typing import Optional, List, Tuple

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.runner.get_execution_plan import get_execution_plan
from drkns.runner.run_plan import run_plan
from drkns.runner.get_successful_flag_and_combined_output import\
    get_successful_flag_and_combined_output


def run(
        root_config_unit: ConfigUnit,
        target_step_name: Optional[str] = None,
        summary: bool = False,
        limit_output: bool = False) \
        -> Tuple[int, List[str]]:
    plan = get_execution_plan(root_config_unit, target_step_name)
    status_history = run_plan(plan)
    return get_successful_flag_and_combined_output(
        status_history, summary, limit_output)
