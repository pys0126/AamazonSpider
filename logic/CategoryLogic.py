from util.MysqlUtil import session
from model.CategoryModel import CategoryModel
from util.StringUtil import urldecode


def category_info_list() -> list[dict]:
    """
    获取所有类别信息
    :return: 类别信息列表
    """
    return [vars(category) for category in session.query(CategoryModel).all()]


def category_name_list() -> list[str]:
    """
    获取所有类别信息名称，用于搜索
    :return: 类别名称列表
    """
    return [vars(category).get("name") for category in session.query(CategoryModel).all()]


def category_id_by_name(name: str) -> int:
    """
    根据名称获取ID
    :param name: 名称
    :return: ID
    """
    name: str = urldecode(text=name.replace("and", "&"))
    result: CategoryModel = session.query(CategoryModel).filter(CategoryModel.name.like(f"{name}%")).first()
    return result.id
