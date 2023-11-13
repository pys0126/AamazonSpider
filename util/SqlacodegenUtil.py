import os


def gen_model(database_name: str, table_name: str, output_path: str, host: str = "localhost", port: int = 3306,
              username: str = "root", password: str = "root") -> None:
    """
    生成sqlalchemy的Model
    :param host: Mysql主机
    :param port: Mysql端口
    :param username: 用户名
    :param password: 密码
    :param database_name: 数据库名
    :param table_name: 表名
    :param output_path: 输出路径
    :return:
    """
    cmd: str = f"sqlacodegen --tables {table_name} " \
               f"'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}' > " \
               f"{output_path}"
    os.system(cmd)
