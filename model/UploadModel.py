from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from util.TimeUtil import now_timestamp
from model.BaseModel import BaseModel


class UploadModel(BaseModel):
    __tablename__ = 'uploads'

    id = Column(INTEGER(11), primary_key=True)
    file_original_name = Column(String(255))  # 图片名称
    file_name = Column(String(255))  # 图片URL
    user_id = Column(INTEGER(11), default=9)
    file_size = Column(INTEGER(11))  # 图片大小
    extension = Column(String(10))  # 图片后缀
    type = Column(String(15), default="image")
    external_link = Column(String(500))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    deleted_at = Column(TIMESTAMP)
    mid = Column(BIGINT(20), nullable=False, default=now_timestamp())
