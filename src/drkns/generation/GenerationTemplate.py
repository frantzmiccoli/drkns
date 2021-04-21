

class GenerationTemplate:

    def __init__(
            self,
            source_path: str,
            template: str,
            group_template: str,
            unit_template: str
    ):
        self.source_path: str = source_path
        self.template: str = template
        self.group_template: str = group_template
        self.unit_template: str = unit_template
