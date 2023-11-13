from config import YAML_CONTENT
from logic.CategoryLogic import category_name_list

# 获取爬虫配置
SPIDER_CONFIG: dict = YAML_CONTENT.get("SpiderConfig")


class SpiderConfig:
    """
    爬虫配置
    """
    search_list: list[str] = category_name_list()  # 搜索关键词列表
    spider_worker: int = int(SPIDER_CONFIG.get("spider_worker"))  # 爬虫线程数
    spider_size: int = int(SPIDER_CONFIG.get("spider_size"))  # 爬取数量
    search_url_template: str = SPIDER_CONFIG.get("search_url_template")  # 爬取URL模板
    proxies: bool = SPIDER_CONFIG.get("proxies")  # 是否开启代理
    proxies_url: str = SPIDER_CONFIG.get("proxies_url")  # 代理URL

    @property
    def home_url(self) -> str:
        """
        主页URL
        :return:
        """
        home_url: str = SPIDER_CONFIG.get("home_url")
        if home_url.endswith("/"):
            return home_url[:-1]
        else:
            return home_url

    @property
    def spider_url_list(self) -> list[str]:
        """
        爬取的URL列表
        :return: URL列表
        """
        spider_url_list: list = []
        for category_name in category_name_list():
            spider_url_list.append(SpiderConfig.search_url_template.format(category_name.replace("&", "and")))
        return spider_url_list
