from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.generation._tags import all_group_names_tag, groups_tag
from drkns.generation.generation.get_group_block import get_group_block
from drkns.generation.GenerationTemplate import GenerationTemplate
from drkns.generation.pattern_util import format_list_in_template


def get_formatted_from_groups_configuration(
        generation_template: GenerationTemplate,
        groups: list[tuple[str, list[ConfigUnit], list[str]]]
) -> str:
    group_blocks = []
    all_group_names = []
    for group_name, group_config_units, dependency_groups_name in groups:
        group_block = get_group_block(
            generation_template, group_name, group_config_units,
            dependency_groups_name)
        group_blocks.append(group_block)

        all_group_names.append(group_name)

    formatted = generation_template.template
    formatted = format_list_in_template(
        groups_tag, group_blocks, formatted, line_level=True)

    formatted = format_list_in_template(
        all_group_names_tag, all_group_names, formatted, line_level=False)

    return formatted
