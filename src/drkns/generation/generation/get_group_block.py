from typing import List

import os


from drkns.util import get_longest_common_prefix
from drkns.configunit.ConfigUnit import ConfigUnit
from drkns.generation.GenerationTemplate import GenerationTemplate
from drkns.generation.generation.get_unit_block import get_unit_block
from drkns.generation.pattern_util \
    import format_list_in_template, get_pattern_from_tag, \
        format_list_optional_in_template
from drkns.generation._tags \
    import group_units_tag, group_name_tag, dependency_groups_names_tag


def get_group_block(
        generation_template: GenerationTemplate,
        group_name: str,
        group_config_units: List[ConfigUnit],
        dependency_group_names: List[str]
) -> str:
    formatted_config_units = [
        get_unit_block(generation_template, config_unit)
        for config_unit in group_config_units
    ]
    formatted_group = generation_template.group_template
    formatted_group = format_list_in_template(
        group_units_tag, formatted_config_units, formatted_group,
        line_level=True)
    formatted_group = format_list_in_template(
        dependency_groups_names_tag,
        dependency_group_names,
        formatted_group, line_level=False)
    formatted_group = format_list_optional_in_template(
        dependency_groups_names_tag,dependency_group_names, formatted_group)

    formatted_group = formatted_group.replace(
        get_pattern_from_tag(group_name_tag), group_name)

    return formatted_group


def _get_group_name(
        generation_template: GenerationTemplate,
        group_config_units: List[ConfigUnit]
) -> str:
    truncated_directories = []
    names = []

    template_root_directory = os.path.abspath(generation_template.source_path)
    for config_unit in group_config_units:
        unit_directory = os.path.abspath(config_unit.directory)
        unit_directory = unit_directory.replace(
            template_root_directory, unit_directory)
        truncated_directories.append(unit_directory)

        names.append(config_unit.name)

    prefix = get_longest_common_prefix(truncated_directories)
    names_string = ', '.join(names)
    if len(names) > 1:
        names_string = '{' + names_string + '}'

    return prefix + names_string





