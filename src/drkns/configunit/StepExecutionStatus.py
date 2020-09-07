class StepExecutionStatus:

    def __init__(self, step_name: str, successful: bool, output: str):
        self.step_name: str = step_name
        self.successful: bool = successful
        self.output: str = output
