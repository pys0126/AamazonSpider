from sqlalchemy import Column, DECIMAL, String, Text, INTEGER
from sqlalchemy.dialects.mysql import LONGTEXT
from model import BaseModel


class ProductModel(BaseModel):
    """
    商品表
    """
    __tablename__ = "product"  # 表名

    id = Column(String(32), primary_key=True, comment="主键")
    title = Column(String(200), comment="商品标题")
    keyword = Column(String(50), comment="商品关键词")
    images = Column(Text, comment="商品图片列表，用英文','分割")
    price = Column(DECIMAL(20, 2), comment="商品单价")
    url = Column(Text, comment="商品详情页地址")
    description = Column(LONGTEXT, comment="商品详情")
    create_time = Column(INTEGER, comment="创建时间戳")
    update_time = Column(INTEGER, comment="更新时间戳")
