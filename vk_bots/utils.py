"""
VK Bots API Wrapper
Copyright (c) 2020-2021 Misaal
"""

import json
import random
from collections import namedtuple


def to_namedtuple(name, data):
    """Function used to convert any data to namedtuple object"""

    def _json_object_hook(obj):
        return namedtuple(name, obj.keys())(*obj.values())

    data = json.dumps(data)  # crutch required to parse inner dicts as well
    return json.loads(data, object_hook=_json_object_hook)


def get_random_id():
    return random.randrange(-2147483648, 2147483648)
