"""
VK Bots API Wrapper
Copyright (c) 2020-2021 Misaal
"""

import asyncio
import json
import typing

import aiohttp

from .errors import VKAPIError
from .utils import to_namedtuple
from .api import Api, ApiOld

available_events = (
    # Common
    'ready',

    # Messages
    'message_new',
    'message_reply',
    'message_edit',
    'message_allow',
    'message_deny',
    'message_typing_state',
    'message_event',

    # Photos
    'photo_new',
    'photo_comment_new',
    'photo_comment_edit',
    'photo_comment_restore',
    'photo_comment_delete',

    # Audios
    'audio_new',

    # Videos
    'video_new',
    'video_comment_new',
    'video_comment_edit',
    'video_comment_restore',
    'video_comment_delete',

    # Wall
    'wall_post_new',
    'wall_repost',
    'wall_reply_new',
    'wall_reply_edit',
    'wall_reply_restore',
    'wall_reply_delete',

    # Likes
    'like_add',
    'like_remove',

    # Boards
    'board_post_new',
    'board_post_edit',
    'board_post_restore',
    'board_post_delete',

    # Market
    'market_comment_new',
    'market_comment_edit',
    'market_comment_restore',
    'market_comment_delete',
    'market_order_new',
    'market_order_edit',

    # Users
    'group_leave',
    'group_join',
    'user_block',
    'user_unblock',

    # Misc
    'poll_vote_new',
    'group_officers_edit',
    'group_change_settings',
    'group_change_photo',
    'vkpay_transaction',
    'app_payload',

    # Donut
    'donut_subscription_create',
    'donut_subscription_prolonged',
    'donut_subscription_expired',
    'donut_subscription_cancelled',
    'donut_subscription_price_changed',
    'donut_money_withdraw',
    'donut_money_withdraw_error',
)


class _LongPollServer:
    def __init__(self, group_id, access_token, v):
        self.group_id = group_id
        self.access_token = access_token
        self.v = v

        self.server = ''
        self.key = ''
        self.ts = 0

    async def setup(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url='https://api.vk.com/method/groups.getLongPollServer',
                                   params=dict(group_id=self.group_id,
                                               access_token=self.access_token,
                                               v=self.v)) as response:
                data = await response.read()
                data = json.loads(data.decode())

                if 'error' in data:
                    raise VKAPIError(data['error']['error_code'], data['error']['error_msg'])
                else:
                    self.server = data['response']['server']
                    self.key = data['response']['key']
                    self.ts = data['response']['ts']

    async def _get(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.server,
                                   params=dict(act='a_check',
                                               key=self.key,
                                               ts=self.ts,
                                               wait=25)) as response:
                data = await response.read()
                data = json.loads(data)

                if 'failed' in data:
                    if data['failed'] == 1:
                        self.ts = data['ts']
                    elif data['failed'] in (2, 3):
                        await self.setup()
                else:
                    self.ts = data['ts']
                    for event in data['updates']:
                        yield event

    async def listen(self):
        while True:
            async for event in self._get():
                yield event


class Client:
    """Class representing a client connection to VK"""

    def __init__(self, group_id: int, access_token: str, v: float = 5.131):
        self.group_id = group_id
        self.access_token = access_token
        self.v = v

        self.api = Api(access_token, v)
        self.api_old = ApiOld(access_token, v)

        self._long_poll = None
        self.loop = None

    def event(self, coro: typing.Any):
        """Decorator used to register events"""

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be coroutine')

        if coro.__name__ not in available_events:
            raise TypeError('unknown event type')

        self.__setattr__(coro.__name__, coro)

    async def _mainloop(self):
        self.long_poll = _LongPollServer(self.group_id, self.access_token, self.v)
        await self.long_poll.setup()

        if 'ready' in self.__dir__():
            task = asyncio.create_task(self.__getattribute__('ready')())
            asyncio.ensure_future(task)

        async for event in self.long_poll.listen():
            if event['type'] in self.__dir__():
                data = event['object']
                args = list(map(to_namedtuple, data.keys(), data.values()))  # args parsing
                task = self.__getattribute__(event['type'])(*args)
                asyncio.create_task(task)

    def run(self):
        """Function used to run bot"""

        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self._mainloop())
