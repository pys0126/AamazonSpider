from config.SpiderConfig import SpiderConfig
from requests import Response, Session
from DrissionPage import SessionPage
from typing import Union


def get_response_size(url: str) -> int:
    """
    获取响应内容的大小
    :param url: 访问URL
    :return: 内容大小（字节）
    """
    session_page: SessionPage = SessionPage()
    if SpiderConfig.proxies:
        session_page.set.proxies(SpiderConfig.proxies_url)
    session_page.get(url=url)
    response: Union[Response, None] = session_page.response
    if not response:
        raise TimeoutError("请求Response大小出错")
    return int(response.headers.get("Content-Length"))


def fetch(session: Session, url: str, method: str = "GET", data: Union[dict, None] = None,
          cookies: Union[dict, None] = None, user_agent: Union[str, None] = None) -> Response:
    """
    请求方法
    :param session: session对象
    :param url: 请求的URL
    :param method: 请求方法
    :param data: 请求载荷
    :param cookies: cookie
    :param user_agent: UA
    :return: 返回Response
    """
    method: str = method.upper()
    if SpiderConfig.proxies:
        session.proxies = {
            "http": "http://127.0.0.1:8889"
        }
    headers: Union[dict, None] = None
    if user_agent:
        headers = {
            "User-Agent": user_agent
        }
    response: Response = session.request(method=method, url=url, headers=headers, data=data, cookies=cookies)
    return response
