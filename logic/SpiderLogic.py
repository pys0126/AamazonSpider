from logic.ProductLogic import insert_product, query_product_by_name, count_product
from DrissionPage import ChromiumPage, SessionPage
from concurrent.futures import ThreadPoolExecutor
from config.SpiderConfig import SpiderConfig
from typing import Optional, Iterator, Union
from requests import Session, Response
from util.StringUtil import urldecode
from fake_useragent import UserAgent
from lxml.html import Element
from lxml import etree
import json


class SpiderLogic:
    def __init__(self) -> None:
        # 获取每个类别的搜索URL
        self.url_list: list[str] = SpiderConfig().spider_url_list
        # 用于爬取的数量计数
        self.totality: int = 0
        # 创建user_agent，默认随机UA
        self.user_agent: Optional[str] = UserAgent().random
        # 创建cookie
        self.cookie: Optional[dict] = None
        # 创建请求Session
        self.req_session: Session = Session()
        # 创建SessionPage
        self.session_page: SessionPage = SessionPage()

    def set_header(self) -> None:
        """
        通过浏览器设置请求头
        :return:
        """
        # 创建Chromium
        chromium_page: ChromiumPage = ChromiumPage()
        chromium_page.get(url=SpiderConfig().home_url)  # 请求亚马逊主页
        chromium_page.set.load_strategy.eager()  # 设置加载DOM就停止
        self.cookie = chromium_page.get_cookies(all_domains=True, all_info=True, as_dict=True)  # 设置Cookie
        # self.user_agent = chromium_page.user_agent  # 设置UA
        chromium_page.quit()  # 关闭浏览器
        # 设置requests请求头
        self.session_page.set.cookies(self.cookie)
        self.session_page.set.user_agent(self.user_agent)
        if SpiderConfig.proxies:
            self.session_page.set.proxies(SpiderConfig.proxies_url)

    def simple_fetch(self, url: str) -> Union[Response, None]:
        """
        简易请求方法
        :param url: 请求的URL
        :return: Response
        """
        self.session_page.get(url=url)
        response: Union[Response, None] = self.session_page.response
        return response

    def search_page(self, url: str) -> Union[str, None]:
        """
        获取搜索页面HTML
        :param url: 搜索URL
        :return: HTML
        """
        # 请求URL
        response: Response = self.simple_fetch(url=url)
        if response and response.status_code == 200:
            return response.text
        else:
            chromium_page: ChromiumPage = ChromiumPage()
            chromium_page.get(url=url)
            chromium_page.set.load_strategy.eager()  # 设置加载DOM就停止
            html: str = chromium_page.html
            self.cookie = chromium_page.get_cookies(all_domains=True, all_info=True, as_dict=True)  # 设置Cookie
            self.user_agent = chromium_page.user_agent  # 设置UA
            chromium_page.quit()  # 关闭浏览器
            return html

    def get_all_search_page(self) -> list[str]:
        """
        获取所有搜索页的HTML
        :return: HTML代码列表
        """
        # 设置一次请求头
        self.set_header()
        search_html_list: list[Union[str, None]] = []
        for url in self.url_list:
            print(url)
            result: Union[str, None] = self.search_page(url=url)
            search_html_list.append(result)
        return search_html_list

    def now_search_all_page(self, search_html: str) -> Union[list[str], None]:
        """
        获取当前搜索对象所有的页面URL
        :param search_html: 搜索页面HTML
        :return: 所有的页面URL
        """
        element: Element = etree.HTML(text=search_html)
        total_pages: int = int(element.xpath('//span[@class="s-pagination-item s-pagination-disabled"]/text()')[0])
        # 创建一个存储所有页URL的列表
        all_page_url: list[str] = []
        # 获取下页URL当模板
        next_page_url: str = element.xpath(
            '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href')[0]
        # 从1开始遍历总页数
        for page_size in range(1, total_pages + 1):
            before_url: str = next_page_url.split("page=")[0]  # 前部分URL
            back_url: str = next_page_url.split("page=")[-1][1:]  # 去掉页码后的URL
            result_url: str = SpiderConfig().home_url + before_url + "page=" + str(page_size) + back_url  # 拼接后的URL
            result_url = result_url.replace("/-/zh", "").split("&qid")[0] + "&s=relevanceblender"
            all_page_url.append(result_url)
        return all_page_url

    def product_card_list(self, html: str) -> Union[list[Element], None]:
        """
        获取所有商品板块元素
        :param html: HTML源码
        :return: 商品板块元素列表
        """
        # 页面Element对象
        element: Element = etree.HTML(text=html)
        card_list: list[Element] = element.xpath('//div[@class="a-section a-spacing-base"]')
        return card_list

    def parse_product(self, element: Element) -> Union[dict, None]:
        """
        解析商品
        :param element: 商品板块元素
        :return: 商品字典，或者None
        """
        # 商品名称
        product_name: str = element.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()')[0]
        if not query_product_by_name(title=product_name):  # 如果库中不存在此商品
            # 商品单价
            unit_price_origin: list = element.xpath('.//span[@class="a-price"]/span[@class="a-offscreen"]/text()')
            # 如果找到商品单价
            if unit_price_origin:
                unit_price: float = float(unit_price_origin[0].split("$")[-1].replace(",", ""))
                thumbnail_img: str = element.xpath('.//img[@class="s-image"]/@src')[0]  # 缩略图URL
                # 商品详情页URL
                info_url: str = SpiderConfig().home_url + element.xpath(
                    './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style '
                    'a-text-normal"]/@href ')[0]
                print("正在爬取的商品URL：", info_url)
                # 请求详情页
                info_response: Union[Response, None] = self.simple_fetch(url=info_url)
                if not info_response:
                    return None
                else:
                    info_html: str = info_response.text
                # 详情页Element对象
                info_element: Element = etree.HTML(text=info_html)
                # 获取所有script标签
                script_list: list[Element] = info_element.xpath('//script[@type="text/javascript"]')
                try:
                    # 找到图片详情原始数据
                    info_data_str: str = [script.text for script in script_list if "ImageBlockATF" in script.text][0]
                    # 将图片详情转为字典
                    info_data: dict = json.loads(
                        info_data_str.split("'colorImages': ")[-1].split(",\n")[0].replace(" ", "").replace("'", "\""))
                    # 创建一个存储图片URL的列表
                    image_list: list = []
                    # 遍历所有图片信息，获取图片URL
                    for image_dict in info_data.get("initial"):
                        image_url: Union[str, None] = image_dict.get("hiRes")
                        # 如果hiRes有图片信息
                        if image_url:
                            image_list.append(image_url)
                except (TypeError, IndexError) as _:  # 如果出错，则选择缩略图作为主图和详情图
                    image_list: list = [thumbnail_img]
                # 获取当前的搜索关键词
                keyword: str = info_url.split("keywords=")[-1].split("&")[0].replace("+", " ")
                # 获取商品信息
                description_element: Union[Element, None] = info_element.xpath('//table[@id="productDetails_detailBullets_sections1"]')
                # 如果商品信息不存在则设置为空字符串
                if description_element:
                    description: str = etree.tostring(description_element[0])
                else:
                    description: str = ""
                product_data: dict = {
                    "title": product_name,  # 商品名称
                    "images": image_list,  # 主图URL列表
                    "keyword": keyword,  # 类别ID
                    "price": unit_price,  # 单价
                    "url": info_url,  # 详情页URL
                    "description": description  # 商品详情
                }
                return product_data

    def controls(self, search_html: str) -> None:
        """
        控制器方法，串通各逻辑
        :param search_html: 传来的搜索页HTML
        """
        all_page_url: list = self.now_search_all_page(search_html=search_html)
        for page_url in all_page_url:
            if page_url:
                print("当前页面：", page_url)
                page_response: Union[Response, None] = self.simple_fetch(url=page_url)
                if not page_response:
                    # 创建Chromium
                    chromium_page: ChromiumPage = ChromiumPage()
                    chromium_page.get(url=page_url)  # 请求
                    chromium_page.set.load_strategy.eager()  # 设置加载DOM就停止
                    self.cookie = chromium_page.get_cookies(all_domains=True, all_info=True, as_dict=True)  # 设置Cookie
                    page_html: str = chromium_page.html
                    chromium_page.quit()
                else:
                    page_html: str = page_response.text
                # 获取所有商品板块元素
                product_card_list: list[Element] = self.product_card_list(html=page_html)
                # 多线程爬取
                with ThreadPoolExecutor(max_workers=SpiderConfig.spider_worker) as executor:
                    results: Iterator[Union[dict, None]] = executor.map(self.parse_and_save, product_card_list)
                for result in results:
                    if result:  # 不为None
                        try:
                            # 存入商品表
                            if insert_product(**result):
                                print("商品", result.get("title"), "已入库")
                        except TimeoutError as e:
                            print(e)
                            continue

    def start(self) -> None:
        print("正在汇总URL，请稍等...")
        while True:
            search_html_list: list[Union[str, None]] = self.get_all_search_page()
            search_html_list = [search_html for search_html in search_html_list if search_html]
            print("关键词数量：", len(search_html_list))
            for search_html in search_html_list:
                self.controls(search_html=search_html)
                self.totality = count_product()
                print("当前爬取数量: ", self.totality)
            # 如果总数量大于设定的数量则退出，否则继续爬取
            if self.totality >= SpiderConfig.spider_size:
                break
        print("已完成任务，实际完成数量：", self.totality)
