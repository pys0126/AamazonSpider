# AmazonSpider - 亚马逊采集

*注意：仅供学习，切勿用于非法用途。*

基于 **[DrissionPage](https://gitee.com/g1879/DrissionPage) + [SQLAlchemy](https://www.sqlalchemy.org/) + [lxml](https://pypi.org/project/lxml/)** 的多线程爬虫（需要Chrome浏览器）

## 采集内容

- 商品名称
- 商品价格
- 商品链接
- 商品图片链接
- 商品详情

## 功能

- 可以指定关键词爬取商品信息
- 可以指定线程数量
- 可以指定代理
- 使用`sqlacodegen`通过数据表生成对象
- 使用`SQLAlchemy ORM`框架操作数据库，详情查看`model`包

## 配置

参考`config.yaml`：

```yaml
# 数据库配置
DatabaseConfig:
  # Mysql配置
  MysqlConfig:
    host: 127.0.0.1  # 主机
    port: 3306  # 端口
    database_name: aamazon_spider  # 数据库名称
    username: root  # 用户名
    password: root  # 密码

  # Sqlalchemy配置
  SqlalchemyConfig:
    on_echo: false  # 是否开启查询日志

# 爬虫配置
SpiderConfig:
  # 关键词列表
  keywords:
    - 玩具
    - 电脑
    - 手机
  # 爬取数量（条）
  spider_size: 1000
  # 爬虫线程数，网速快可以设置多一点
  spider_worker: 8
  # 爬取URL模板
  search_url_template: https://www.amazon.com/s?k={}
  # 主页URL
  home_url: https://www.amazon.com
  # 是否开启代理
  proxies: true
  # 代理URL
  proxies_url: http://127.0.0.1:8889
```

## 运行

- 安装依赖 `pip install -r requirements.txt`
- 通过数据表生成对象 `python sql2object.py`
- 通过对象生成数据表 `python object2sql.py`
- 爬虫，启动！`python main.py`
