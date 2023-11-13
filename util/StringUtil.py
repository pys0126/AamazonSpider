from urllib.parse import unquote


def urldecode(text: str) -> str:
    """
    解码URL
    :param text: 原始URL
    :return: 解码后
    """
    decoded_string = unquote(text)
    return decoded_string
