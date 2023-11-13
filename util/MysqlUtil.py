from sqlalchemy import create_engine
from model.BaseModel import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from config.DatabaseConfig import MysqlConfig, SqlalchemyConfig


class MysqlUtil:
    # 构造连接URI
    connect_uri: str = f"mysql+pymysql://" \
                       f"{MysqlConfig.username}:{MysqlConfig.password}@" \
                       f"{MysqlConfig.host}:{MysqlConfig.port}/" \
                       f"{MysqlConfig.database_name}"
    # 初始化数据库连接
    engine: Engine = create_engine(url=connect_uri, echo=SqlalchemyConfig.on_echo)

    @staticmethod
    def create_tables() -> None:
        """
        创建数据表（如果不存在）
        :return:
        """
        # 创建数据表，一方面通过engine来连接数据库，另一方面根据哪些类继承了Base来决定创建哪些表
        # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
        BaseModel.metadata.create_all(MysqlUtil.engine, checkfirst=True)

    @staticmethod
    def session() -> Session:
        """
        获得sqlalchemy回话，用于操作数据库
        :return: Session对象
        """
        # 创建db_session类型
        db_session: sessionmaker = sessionmaker(bind=MysqlUtil.engine)
        return db_session()


# 获取sqlalchemy的Session对象
session: Session = MysqlUtil.session()
