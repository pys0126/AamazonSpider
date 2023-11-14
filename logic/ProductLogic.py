from config import lock
from typing import Union
from util.MysqlUtil import session
from util.TimeUtil import now_timestamp
from model.ProductModel import ProductModel
from util.StringUtil import create_uuid, urldecode


def count_product() -> int:
    """
    商品计数
    :return: 数量
    """
    return len(session.query(ProductModel).all())


def query_product_by_name(title: str) -> Union[ProductModel, None]:
    """
    根据名称查询商品
    :param title: 名称
    :return: 商品或者None
    """
    lock.acquire()
    result: Union[ProductModel, None] = session.query(ProductModel).filter_by(title=title).first()
    lock.release()
    return result


def insert_product(title: str, keyword: str, images: list, price: float, description: str, url: str) -> bool:
    """
    插入商品
    :param title: 名称
    :param keyword: 关键词
    :param images: 图片URL列表
    :param price: 价格
    :param description: 详情
    :param url: 商品详情连接
    :return: 是否成功插入
    """
    # 如果数据库中已有该记录，则直接返回
    if query_product_by_name(title=title):
        return True
    # 保存商品
    product: ProductModel = ProductModel(
        title=title,
        keyword=urldecode(text=keyword),
        images=",".join(images),
        price=price,
        url=url,
        description=description,
        id=create_uuid(),
        create_time=now_timestamp(),
        update_time=now_timestamp()
    )
    try:
        session.add(product)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return False
    return True
