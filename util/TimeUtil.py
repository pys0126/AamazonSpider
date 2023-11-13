import time
from datetime import datetime


def now_format_datetime() -> str:
    """
    获取当前格式化时间字符串
    :return: 当前格式化时间字符串
    """
    # 获取当前时间
    current_time = datetime.now()
    # 格式化时间
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def now_timestamp() -> int:
    """
    获取当前时间戳
    :return: 当前时间戳整数
    """
    return int(time.time())