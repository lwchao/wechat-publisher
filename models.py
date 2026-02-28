"""数据模型操作"""
from database import Article, PublishLog, Config, SessionLocal
from datetime import datetime

def get_all_articles():
    db = SessionLocal()
    try:
        return db.query(Article).order_by(Article.updated_at.desc()).all()
    finally:
        db.close()

def get_article_by_id(article_id):
    db = SessionLocal()
    try:
        return db.query(Article).filter(Article.id == article_id).first()
    finally:
        db.close()

def create_article(data):
    db = SessionLocal()
    try:
        article = Article(
            title=data.get('title', '无标题'),
            author=data.get('author', '匿名'),
            category=data.get('category', '未分类'),
            summary=data.get('summary', ''),
            content=data.get('content', ''),
            cover_image=data.get('cover_image', ''),
            source_file=data.get('source_file', ''),
            status=data.get('status', 'draft')
        )
        db.add(article)
        db.commit()
        db.refresh(article)
        return article
    finally:
        db.close()

def update_article(article_id, data):
    db = SessionLocal()
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            for key, value in data.items():
                if hasattr(article, key):
                    setattr(article, key, value)
            article.updated_at = datetime.now()
            db.commit()
            db.refresh(article)
        return article
    finally:
        db.close()

def delete_article(article_id):
    db = SessionLocal()
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            db.delete(article)
            db.commit()
        return True
    finally:
        db.close()

def create_publish_log(article_id, mode, media_id, result):
    db = SessionLocal()
    try:
        log = PublishLog(article_id=article_id, mode=mode, wechat_media_id=media_id, result=result)
        db.add(log)
        db.commit()
        return log
    finally:
        db.close()

def get_publish_logs(limit=50):
    db = SessionLocal()
    try:
        return db.query(PublishLog).order_by(PublishLog.published_at.desc()).limit(limit).all()
    finally:
        db.close()
