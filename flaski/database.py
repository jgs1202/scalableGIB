# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# wiki.dbという名前のdbファイルの作成を指定
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'wiki.db')
# sqlliteを指定して、テーブルのcreateを指定。
engine = create_engine('sqlite:///' + databese_file, convert_unicode=False)
# bindにテーブルcreateを指定。
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# declarative_baseのインスタンス生成。
Base = declarative_base()
# 実行用のセッション格納？
Base.query = db_session.query_property()


def init_db():
    import flaski.models
    # Baseの内容でcreate実行？
    Base.metadata.create_all(bind=engine)

# # -*- coding: utf-8 -*-
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import MetaData
#
#
# # dbとの接続関連の処理
# engine = create_engine('mysql://username:password@localhost/dbname?charset=utf8')
# Base = declarative_base()
# metadata = MetaData()
# Session = sessionmaker(bind=engine)
# session = Session()
