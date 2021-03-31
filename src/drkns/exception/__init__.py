
class UnknownDependencyException(Exception):
    pass


class UnknownStepException(Exception):
    pass


class UnknownCommandException(Exception):
    pass


class UnknownCommandFlagException(Exception):
    pass


class MalformedIgnorePatternException(Exception):
    pass


class CircularDependencyException(Exception):
    pass


class MissingCommandException(Exception):
    pass


class MissingForgetTargetException(Exception):
    pass


class MissingSyncDirectionException(Exception):
    pass


class MissingS3PathException(Exception):
    pass
