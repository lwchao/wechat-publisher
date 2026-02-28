"""SQLite 数据库操作模块"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(50), default='匿名')
    category = Column(String(50), default='未分类')
    summary = Column(Text)
    content = Column(Text, nullable=False)
    cover_image = Column(String(500))
    source_file = Column(String(200))
    status = Column(String(20), default='draft')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class PublishLog(Base):
    __tablename__ = 'publish_logs'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer)
    mode = Column(String(20))
    wechat_media_id = Column(String(100))
    published_at = Column(DateTime, default=datetime.now)
    result = Column(Text)

class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    value = Column(Text)

DB_PATH = os.environ.get('DB_PATH', 'wechat.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
