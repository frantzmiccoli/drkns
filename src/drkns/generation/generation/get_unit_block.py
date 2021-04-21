from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.generation.GenerationTemplate import GenerationTemplate
from drkns.generation.pattern_util import get_pattern_from_tag
from drkns.generation._tags import unit_name_tag


def get_unit_block(
        generation_template: GenerationTemplate,
        config_unit: ConfigUnit
) -> str:
    unit_name = config_unit.name
    unit_template = generation_template.unit_template
    unit_name_pattern = get_pattern_from_tag(unit_name_tag)
    return unit_template.replace(unit_name_pattern, unit_name)
