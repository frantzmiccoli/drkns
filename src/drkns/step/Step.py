# noqa: N999


class Step:

    def __init__(self, data: dict | str):
        if not isinstance(data, dict):
            data = {
                'command': data,
                'background': False
            }

        self.command: str = data['command']
        self.background: bool = data.get('background', False)
