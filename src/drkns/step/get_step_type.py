from drkns.configunit.ConfigUnit import ConfigUnit
import drkns.step.step_type as step_type


def get_step_type(config_unit: ConfigUnit, step_name: str) -> str:
    for possible_step_type in step_type.types:
        step_names = config_unit.get_steps(possible_step_type)
        if step_name in step_names:
            return possible_step_type

    raise Exception('Unable to resolve type for step ' + step_name +
                    ' in ConfigUnit ' + config_unit.name)
