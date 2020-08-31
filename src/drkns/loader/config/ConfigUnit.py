import os
import checksumdir


class ConfigUnit:

    def __init__(self, name, data):
        self.name = name
        self.directory = data.directory
        self.steps = data.get('steps', {})
        self.dependencies = {}

        self._hash = None

    def get_hash(self):
        if self._hash is None:
            self._hash = checksumdir.dirhash(self.directory)

        return self._hash

    def get_error_string(self):
        errors = self._get_errors()

        if len(errors) == 0:
            return None

        return 'Error in "' + self.name + '":\n' + '\n\t'.join(errors) + '\n\n'

    def _get_errors(self):
        errors = []
        if self.directory is None:
            errors.append(self.name + ': directory is not set')
        elif not os.path.exists(self.directory):
            errors.append(self.name + ': directory does not exist')
        if self.steps.length == 0:
            errors.append(self.name + ': no steps are defined')

        for name, dependency in self.dependencies.items():
            dependency_error_string = dependency.get_error_string()
            if dependency_error_string is not None:
                errors = dependency_error_string

        return errors

