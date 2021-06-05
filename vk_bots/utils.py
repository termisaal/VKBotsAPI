"""
VK Bots API Wrapper
Copyright (c) 2020-2021 termisaal
"""

import json
import random
import typing
from collections import namedtuple


def to_namedtuple(name: str, data: typing.Any) -> typing.Any:
    """Function used to convert any data to namedtuple object"""

    def _json_object_hook(obj: typing.Any) -> typing.Any:
        return namedtuple(name, obj.keys())(*obj.values())

    data = json.dumps(data)  # crutch required to parse inner dicts as well
    return json.loads(data, object_hook=_json_object_hook)


def random_id():
    return random.randrange(-2147483648, 2147483647)
