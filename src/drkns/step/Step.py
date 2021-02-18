from typing import Union, Dict


class Step:

    def __init__(self, data: Union[Dict,str]):
        if not isinstance(data, dict):
            data = {
                'command': data,
                'background': False
            }

        self.command: str = data['command']
        self.background: bool = data.get('background', False)
