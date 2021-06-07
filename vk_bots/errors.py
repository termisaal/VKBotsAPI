"""
VK Bots API Wrapper
Copyright (c) 2020-2021 Misaal
"""


class VKAPIError(Exception):
    """Base class for VK API errors"""
    def __init__(self, error_code, error_msg):
        """

        :param int error_code:
        :param str error_msg:
        """
        message = str(error_code) + f' ({error_msg})'
        super().__init__(message)
