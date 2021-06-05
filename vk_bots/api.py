"""
VK Bots API Wrapper
Copyright (c) 2020-2021 termisaal
"""

import aiohttp
import json

from .errors import VKAPIError
from .utils import to_namedtuple


class Api:
    __slots__ = ('_method', '_access_token', '_v')

    def __init__(self, access_token: str, v: float = 5.131, _method=None):
        self._access_token = access_token
        self._v = v

        if _method is None:
            _method = []
        self._method = _method

    def __getattr__(self, item):
        return Api(self._access_token, self._v, self._method + [item])

    async def __call__(self, **kwargs):
        kwargs['access_token'] = self._access_token
        kwargs['v'] = self._v
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'https://api.vk.com/method/{".".join(self._method)}',
                                   params=kwargs) as response:
                data = await response.read()
                data = json.loads(data.decode())

                if 'error' in data:
                    raise VKAPIError(data['error']['error_code'], data['error']['error_msg'])

                return to_namedtuple('response', data)
