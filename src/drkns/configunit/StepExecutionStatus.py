class StepExecutionStatus:

    def __init__(
            self,
            step_name: str,
            successful: bool = None,
            ignored: bool = None,
            output: str = None
    ):
        if successful is None:
            successful = False

        if ignored is None:
            ignored = False

        if output is None:
            output = None

        self.step_name: str = step_name
        self.successful: bool = successful
        self.ignored: bool = ignored
        self.output: str = output
