from util.MysqlUtil import session
from model.UploadModel import UploadModel
from util.RequestsUtil import get_response_size


def file_name_by_id(image_id: int) -> str:
    """
    根据ID查询图片连接
    :param image_id: 图片ID
    :return: 图片连接
    """
    upload: UploadModel = session.query(UploadModel).filter_by(id=image_id).first()
    return upload.file_name


def insert_upload(file_name: str) -> int:
    """
    插入图片信息
    :param file_name: 图片URL
    :return: 图片ID
    """
    # 如果已存在该记录直接返回该记录的ID
    upload: UploadModel = session.query(UploadModel).filter_by(file_name=file_name).first()
    if upload:
        return upload.id
    file_original_name: str = file_name.split("/")[-1]  # 图片名称
    # file_size: int = get_response_size(url=file_name)  # 图片大小
    file_size: int = 10240000  # 图片大小，占时固定
    extension: str = file_original_name.rsplit(".")[-1]  # 图片后缀
    # 插入数据
    upload: UploadModel = UploadModel(
        file_original_name=file_original_name,
        file_size=file_size,
        file_name=file_name,
        extension=extension
    )
    try:
        session.add(upload)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return 0
    upload_id: int = upload.id
    # 返回插入数据的ID
    return upload_id
