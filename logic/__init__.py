from logic.SpiderLogic import SpiderLogic


def start() -> None:
    """
    启动爬虫
    :return:
    """
    spider: SpiderLogic = SpiderLogic()  # 实例化亚马逊爬虫类
    spider.start()  # 启动亚马逊爬虫
