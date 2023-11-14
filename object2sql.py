"""
对象转数据表
"""
from util.MysqlUtil import MysqlUtil

if __name__ == "__main__":
    # 导入需要创建表的对象
    from model.ProductModel import ProductModel
    # 创建表
    MysqlUtil.create_tables()
