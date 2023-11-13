from sqlalchemy import Column, Float, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from model.BaseModel import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = Column(INTEGER(11), primary_key=True)
    parent_id = Column(INTEGER(11), server_default=text("0"))
    level = Column(INTEGER(11), nullable=False, server_default=text("0"))
    name = Column(String(50), nullable=False)
    order_level = Column(INTEGER(11), nullable=False, server_default=text("0"))
    commision_rate = Column(Float(8, True), nullable=False, server_default=text("0.00"))
    banner = Column(String(100))
    icon = Column(String(100))
    featured = Column(INTEGER(11), nullable=False, server_default=text("0"))
    top = Column(INTEGER(11), nullable=False, server_default=text("0"))
    digital = Column(INTEGER(11), nullable=False, server_default=text("0"))
    slug = Column(String(255), index=True)
    meta_title = Column(String(255))
    meta_description = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    updated_at = Column(TIMESTAMP, server_default=text("current_timestamp()"))
