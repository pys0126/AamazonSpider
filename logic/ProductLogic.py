from config import lock
from typing import Union
from util.MysqlUtil import session
from model.ProductModel import ProductModel
from logic.UploadLogic import file_name_by_id, insert_upload


def count_product() -> int:
    """
    商品计数
    :return: 数量
    """
    return len(session.query(ProductModel).all())


def query_product_by_name(name: str) -> Union[ProductModel, None]:
    """
    根据名称查询商品
    :param name: 名称
    :return: 商品或者None
    """
    lock.acquire()
    result: Union[ProductModel, None] = session.query(ProductModel).filter_by(name=name).first()
    lock.release()
    return result


def insert_product(name: str, category_id: int, photos: list, thumbnail_img: str, unit_price: float) -> bool:
    """
    插入商品
    :param name: 名称
    :param category_id: 分类ID
    :param photos: 图片URL列表
    :param thumbnail_img: 缩略图URL
    :param unit_price: 单价
    :return: 是否成功插入
    """
    # 如果数据库中已有该记录，则直接返回
    if query_product_by_name(name=name):
        return True
    # 将URL列表转为ID列表
    photos: list[str] = [str(insert_upload(file_name=photo)) for photo in photos]
    # 创建一个图片标签列表
    img_tag_list: list = []
    if len(photos) > 2:  # 如果图片大于两张
        product_photos: str = ",".join(photos[:2])
        # 遍历剩下图片
        for photo in photos[2:]:
            # 构建img标签
            photo_src: str = file_name_by_id(image_id=int(photo))
            img_tag: str = f"<img src='{photo_src}'>"
            img_tag_list.append(img_tag)
    else:  # 如果小于两张
        product_photos: str = ",".join(photos)
        # 遍历所有图片
        for photo in photos:
            # 构建img标签
            photo_src: str = file_name_by_id(image_id=int(photo))
            img_tag: str = f"<img src='{photo_src}'>"
            img_tag_list.append(img_tag)
    # 构建多图img标签
    img_src: str = "".join(img_tag_list)
    # 构建html代码
    product_description: str = f"<p>{img_src}</p>"
    # 存入图片库
    thumbnail_img: str = str(insert_upload(file_name=thumbnail_img))
    # 保存商品
    product: ProductModel = ProductModel(
        name=name,
        category_id=category_id,
        photos=thumbnail_img if not product_photos else product_photos,
        thumbnail_img=thumbnail_img,
        description=product_description,
        unit_price=unit_price
    )
    try:
        session.add(product)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return False
    return True
