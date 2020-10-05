from typing import List

from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.configunit.run_step import run_step
from drkns.configunit.StepExecutionStatus import StepExecutionStatus


def cleanup(config_unit: ConfigUnit) -> List[StepExecutionStatus]:
    statuses = []
    for step_name in config_unit.cleanupSteps.keys():
        statuses += run_step(config_unit, step_name, True)
    return statuses

