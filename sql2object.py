"""
数据表转对象
"""
from util.SqlacodegenUtil import gen_model
from config.DatabaseConfig import MysqlConfig

if __name__ == "__main__":
    gen_model(
        database_name=MysqlConfig.database_name,
        table_name="product",
        output_path="./model/ProductModel.py",
        host=MysqlConfig.host,
        port=MysqlConfig.port,
        username=MysqlConfig.username,
        password=MysqlConfig.password
    )