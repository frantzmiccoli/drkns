import os
import re

from drkns.exception import MissingGenerationTemplateDirectoryException, \
    MissingGenerationTemplateException, MultipleGenerationTemplateException


_template_directory = '.drknsgeneration'
_template_file_re = re.compile(r'^.*\.template\..*$')


def get_generation_template_path(from_path: str) -> str:
    template_directory = os.path.join(from_path, _template_directory)
    if not os.path.exists(template_directory):
        error_message = template_directory + ' directory can not be found'
        raise MissingGenerationTemplateDirectoryException(error_message)

    contained_files = os.listdir(template_directory)

    matched_files = []
    for contained_file in contained_files:
        pattern_match = \
            _template_file_re.match(contained_file)
        if pattern_match is None:
            continue

        matched_files.append(contained_file)

    if len(matched_files) == 0:
        error_message = 'No template found in ' + template_directory
        raise MissingGenerationTemplateException(error_message)

    if len(matched_files) > 1:
        error_message = 'Multiple template found in ' + \
                        template_directory + ': ' + ', '.join(matched_files)
        MultipleGenerationTemplateException(error_message)

    return os.path.join(template_directory, matched_files.pop())