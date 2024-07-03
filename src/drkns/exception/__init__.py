
class UnknownDependencyException(Exception):
    pass


class CircularDependencyException(Exception):
    pass


class UnexpectedBranchException(Exception):
    pass


class UnknownStepException(Exception):
    pass


class UnknownCommandException(Exception):
    pass


class UnknownCommandFlagException(Exception):
    pass


class MissingCommandException(Exception):
    pass


class MissingForgetTargetException(Exception):
    pass


class MissingSyncDirectionException(Exception):
    pass


class MissingS3PathException(Exception):
    pass


class MalformedIgnorePatternException(Exception):
    pass


class MissingGenerationTemplateDirectoryException(Exception):
    pass


class MissingGenerationTemplateException(Exception):
    pass


class MultipleGenerationTemplateException(Exception):
    pass


class UnableToParseGenerationTemplateBlock(Exception):
    pass


class MissingGenerationTemplateTag(Exception):
    pass


class UnableToFindPattern(Exception):
    pass


class DependenciesNotAvailable(Exception):
    pass
