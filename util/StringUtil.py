from urllib.parse import unquote
from uuid import uuid4


def urldecode(text: str) -> str:
    """
    解码URL
    :param text: 原始URL
    :return: 解码后
    """
    decoded_string = unquote(text)
    return decoded_string


def create_uuid() -> str:
    """
    创建UUID
    :return: UUID字符串
    """
    return str(uuid4()).replace("-", "")
