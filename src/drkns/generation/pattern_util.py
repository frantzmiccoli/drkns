from typing import List

import re

from drkns.exception import UnableToFindPattern


def format_list_in_template(
        tag: str,
        items: List[str],
        template: str,
        line_level: bool
) -> str:
    list_re = get_list_re_from_tag(tag, line_level)
    list_match = list_re.search(template)
    if list_match is None:
        raise UnableToFindPattern(list_re.pattern)

    separator = list_match.groupdict()['separator']
    joined_items = separator.join(items)
    start_index = list_match.start()
    end_index = list_match.end()
    return template[:start_index] + joined_items + template[end_index:]


def format_list_optional_in_template(
        tag: str,
        items: List,
        template: str
) -> str:
    list_optional_re = get_list_optional_re_from_tag(tag)
    list_optional_match = list_optional_re.search(template)
    if list_optional_match is None:
        raise UnableToFindPattern(list_optional_re.pattern)

    conditional_value = ''
    if len(items) > 0:
        conditional_value = list_optional_match.groupdict()['conditional_value']

    start_index = list_optional_match.start()
    end_index = list_optional_match.end()
    return template[:start_index] + conditional_value + template[end_index:]


def get_list_re_from_tag(tag: str, line_level: bool) -> re.Pattern:
    pattern = get_list_replacement_pattern_from_tag(tag, line_level)
    return re.compile(pattern)


def get_list_optional_re_from_tag(tag: str) -> re.Pattern:
    pattern = r'%' + tag + r'\?\{(?P<conditional_value>.*)\}%'
    return re.compile(pattern)


def get_list_replacement_pattern_from_tag(tag: str, line_level: bool) -> str:
    pattern = '%' + tag + r'\{(?P<separator>.*)\}%'
    if not line_level:
        return pattern
    return _get_line_level_pattern(pattern)


def get_block_re_from_tag_prefix(tag_prefix: str) -> re.Pattern:
    begin_line_pattern = get_line_pattern_from_tag(tag_prefix + 'BEGIN')
    end_line_pattern = get_line_pattern_from_tag(tag_prefix + 'END')
    block_pattern = \
        '(?P<begin_line>' + begin_line_pattern + ')' +\
        '(?P<block>(?:.|\n)*)' +\
        '(?P<end_line>' + end_line_pattern + ')'
    return re.compile(block_pattern)


def get_line_pattern_from_tag(tag: str) -> str:
    return _get_line_level_pattern('%' + tag + '%')


def get_pattern_from_tag(tag: str) -> str:
    return '%' + tag + '%'


def _get_line_level_pattern(pattern: str) -> str:
    return '(?:^|\n).*' + pattern + '.*[\n$]'
