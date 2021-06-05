"""
VK Bots API Wrapper
Copyright (c) 2020-2021 termisaal
"""

import aiohttp
import json
import typing

from .errors import VKAPIError
from .keyboard import Keyboard
from .utils import to_namedtuple, get_random_id


class MethodGroup:
    """Base class for API methods groups"""

    def __init__(self, access_token, v):
        self._access_token = access_token
        self._v = v

    async def _api_request(self, method, **kwargs):
        for key in list(kwargs):
            if kwargs[key] is None:
                kwargs.pop(key)
        kwargs['access_token'] = self._access_token
        kwargs['v'] = self._v

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'https://api.vk.com/method/{method}',
                                   params=kwargs) as response:
                data = await response.read()
                data = json.loads(data)

                if 'error' in data:
                    raise VKAPIError(data['error']['error_code'], data['error']['error_msg'])
                else:
                    return data


class AppWidgets(MethodGroup):
    pass


class Board(MethodGroup):
    pass


class Docs(MethodGroup):
    pass


class Groups(MethodGroup):
    pass


class Market(MethodGroup):
    pass


class Messages(MethodGroup):
    async def createChat(self):
        pass

    async def delete(self):
        pass

    async def deleteChatPhoto(self):
        pass

    async def deleteConversation(self):
        pass

    async def edit(self):
        pass

    async def editChat(self):
        pass

    async def getByConversationMessageId(self):
        pass

    async def getById(self):
        pass

    async def getConversationMembers(self):
        pass

    async def getConversations(self):
        pass

    async def getConversationsById(self):
        pass

    async def getHistory(self):
        pass

    async def getHistoryAttachments(self):
        pass

    async def getImportantMessages(self):
        pass

    async def getIntentUsers(self):
        pass

    async def getInviteLink(self):
        pass

    async def isMessagesFromGroupAllowed(self):
        pass

    async def markAsAnsweredConversation(self):
        pass

    async def markAsImportantConversation(self):
        pass

    async def markAsRead(self):
        pass

    async def pin(self):
        pass

    async def removeChatUser(self):
        pass

    async def restore(self):
        pass

    async def search(self):
        pass

    async def searchConversations(self):
        pass

    async def send(self,
                   user_id: int = None,
                   random_id: int = get_random_id(),
                   peer_id: int = None,
                   peer_ids: typing.Iterable[int] = None,
                   domain: str = None,
                   chat_id: int = None,
                   message: str = None,
                   lat: float = None,
                   long: float = None,
                   attachment: typing.Union[str, typing.Iterable[str]] = None,
                   reply_to: int = None,
                   forward_messages: typing.Union[int, typing.Iterable[int]] = None,
                   forward: dict = None,
                   sticker_id: int = None,
                   keyboard: typing.Union[Keyboard, dict] = None,
                   template: dict = None,
                   payload: str = None,
                   content_source: dict = None,
                   dont_parse_links: typing.Union[bool, int] = None,
                   disable_mentions: typing.Union[bool, int] = None,
                   intent: str = None,
                   subscribe_id: int = None):
        if attachment is not None and type(attachment) != str:
            attachment = ','.join(attachment)
        if forward_messages is not None and type(forward_messages) != int:
            forward_messages = ','.join(map(str, forward_messages))
        if keyboard is not None and type(keyboard) != dict:
            return dict(keyboard)
        if dont_parse_links is not None and type(dont_parse_links) == bool:
            dont_parse_links = int(dont_parse_links)
        if disable_mentions is not None and type(disable_mentions) == bool:
            disable_mentions = int(disable_mentions)

        return await self._api_request('messages.send',
                                       user_id=user_id,
                                       random_id=random_id,
                                       peer_id=peer_id,
                                       peer_ids=peer_ids,
                                       domain=domain,
                                       chat_id=chat_id,
                                       message=message,
                                       lat=lat,
                                       long=long,
                                       attachment=attachment,
                                       reply_to=reply_to,
                                       forward_messages=forward_messages,
                                       forward=forward,
                                       sticker_id=sticker_id,
                                       keyboard=keyboard,
                                       template=template,
                                       payload=payload,
                                       content_source=content_source,
                                       dont_parse_links=dont_parse_links,
                                       disable_mentions=disable_mentions,
                                       intent=intent,
                                       subscribe_id=subscribe_id)

    async def sendMessageEventAnswer(self):
        pass

    async def setActivity(self):
        pass

    async def setChatPhoto(self):
        pass

    async def unpin(self):
        pass


class Photos(MethodGroup):
    pass


class Podcasts(MethodGroup):
    pass


class Storage(MethodGroup):
    pass


class Stories(MethodGroup):
    pass


class Users(MethodGroup):
    pass


class Utils(MethodGroup):
    pass


class Wall(MethodGroup):
    pass


class Api:
    """Class used to perform requests to VK API"""

    def __init__(self, access_token, v):
        self._access_token = access_token
        self._v = v

        self.appWidgets = AppWidgets(access_token, v)
        self.board = Board(access_token, v)
        self.docs = Docs(access_token, v)
        self.groups = Groups(access_token, v)
        self.market = Market(access_token, v)
        self.messages = Messages(access_token, v)
        self.photos = Photos(access_token, v)
        self.podcasts = Podcasts(access_token, v)
        self.storage = Storage(access_token, v)
        self.stories = Stories(access_token, v)
        self.users = Users(access_token, v)
        self.utils = Utils(access_token, v)
        self.wall = Wall(access_token, v)
