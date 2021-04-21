from typing import Tuple


from drkns.generation.templateloading.get_generation_template_path \
    import get_generation_template_path
import drkns.generation.pattern_util as pattern_util
from drkns.generation.GenerationTemplate import GenerationTemplate
from drkns.exception import UnableToParseGenerationTemplateBlock
from drkns.generation._tags import unit_template_tag_prefix, group_template_tag_prefix
from drkns.generation.templateloading.check_generation_template \
    import check_generation_template


def get_generation_template(from_path: str) -> GenerationTemplate:
    with open(get_generation_template_path(from_path)) as handle:
        raw_template = handle.read()
        generation_template = _parse(from_path, raw_template)
        check_generation_template(generation_template)
        return generation_template


def _parse(from_path, raw_template) -> GenerationTemplate:
    unit_template, raw_template =\
        _extract_from_tag_prefix(unit_template_tag_prefix, raw_template)
    group_template, template = \
        _extract_from_tag_prefix(group_template_tag_prefix, raw_template)
    generation_template = GenerationTemplate(
        from_path, template, group_template, unit_template)
    return generation_template


def _extract_from_tag_prefix(tag_prefix: str, content: str) -> Tuple[str, str]:
    block_re = pattern_util.get_block_re_from_tag_prefix(tag_prefix)
    match = block_re.search(content)
    if match is None:
        error_message = 'No block found from prefix ' + tag_prefix
        raise UnableToParseGenerationTemplateBlock(error_message)
    start_index = match.start()
    end_index = match.end()
    _, block, _ = match.groups()
    stripped_content = content[:start_index] + content[end_index:]
    return block, stripped_content
