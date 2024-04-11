# coding:utf-8

# 导入必要的模块
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# 定义数据库操作类
class Database(object):

    def __init__(self, config=None):
        self.__config = config
        # 创建数据库引擎
        self.__engine= self.__create_engine
        # 创建会话工厂
        self.__session_factory = sessionmaker(bind=self.__engine)
        # 创建基本模型
        self.__base_model = declarative_base()
        # 创建数据库会话
        self.__db_session = scoped_session(self.__session_factory)

    # 创建引擎的属性方法
    @property
    def __create_engine(self):
        # 从配置中获取数据库绑定信息
        bind = self.__config.pop("bind", None)
        # 创建并返回数据库引擎
        return create_engine(bind, **self.__config)

    # 返回基本模型的属性方法
    @property
    def Model(self):
        return self.__base_model

    # 返回数据库会话的属性方法
    @property
    def session(self):
        return self.__db_session

    # 返回数据库引擎的属性方法
    @property
    def engine(self):
        return self.__engine

    # 创建所有表的方法
    def create_all(self):
        # 通过基本模型的元数据创建所有表
        self.Model.metadata.create_all(self.__engine)

    # 删除所有表的方法
    def drop_all(self):
        # 通过基本模型的元数据删除所有表
        self.Model.metadata.drop_all(self.__engine)

# 创建基本模型
BaseModel = declarative_base()

# 定义工资邮箱类
class SalaryEmail(BaseModel):
    # 指定表名
    __tablename__ = 'salary_email'

    # 定义列属性
    id = Column(Integer, primary_key=True)
    field_name = Column(String(64), unique=True)
    field_value = Column(String(512))
    memo = Column(String(256))

# 设置数据库的方法
def set_db():
    # 获取数据库根目录
    #DB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_ROOT = os.getcwd()
    # 拼接数据库文件路径
    DB_PATH = os.path.join(DB_ROOT, 'salary.db')

    # 设置数据库配置信息
    config = {
        "bind": 'sqlite:///{}'.format(DB_PATH)
    }

    # 创建数据库操作对象
    db = Database(config=config)
    if not os.path.exists(DB_PATH):
        # 通过基本模型的元数据创建所有表
        BaseModel.metadata.create_all(db.engine)
    return db

# 主程序入口
if __name__ == '__main__':
    # 设置数据库并创建所有表
    db = set_db()
    # BaseModel.metadata.create_all(db.engine)
