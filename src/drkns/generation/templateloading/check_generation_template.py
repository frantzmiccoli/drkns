import re
from typing import Optional


from drkns.exception import MissingGenerationTemplateTag
from drkns.generation.GenerationTemplate import GenerationTemplate
import drkns.generation.pattern_util as pattern_util
from drkns.generation._tags \
    import group_units_tag, group_name_tag, unit_name_tag, \
    dependency_groups_names_tag, all_group_names_tag


def check_generation_template(generation_template: GenerationTemplate):
    errors_candidates = []

    group_name_tag_error = _get_tag_error(
        group_name_tag, generation_template, 'group_template', 'static')
    errors_candidates.append(group_name_tag_error)

    group_units_tag_error = _get_tag_error(
        group_units_tag, generation_template, 'group_template', 'list')
    errors_candidates.append(group_units_tag_error)

    unit_name_tag_error = _get_tag_error(
        unit_name_tag, generation_template, 'unit_template', 'static')
    errors_candidates.append(unit_name_tag_error)

    dependency_groups_names_tag_error = _get_tag_error(
        dependency_groups_names_tag, generation_template, 'group_template',
        'list')
    errors_candidates.append(dependency_groups_names_tag_error)

    all_group_names_tag_error = \
        _get_tag_error(all_group_names_tag, generation_template,
                       'template', 'list')
    errors_candidates.append(all_group_names_tag_error)

    errors = [error for error in errors_candidates if error is not None]
    if len(errors) > 0:
        raise MissingGenerationTemplateTag('\n'.join(errors))


def _get_tag_error(
        tag: str,
        generation_template: GenerationTemplate,
        field: str,
        tag_type: str
) -> Optional[str]:
    search_in_template = getattr(generation_template, field)
    if tag_type == 'static':
        pattern = pattern_util.get_pattern_from_tag(tag)
        if pattern in search_in_template:
            return None
        return 'Missing ' + pattern + ' in ' + field

    tag_re = pattern_util.get_list_re_from_tag(tag, False)
    match = tag_re.search(search_in_template)
    if match is not None:
        return None
    return 'Missing ' + tag_re.pattern + ' in ' + field

