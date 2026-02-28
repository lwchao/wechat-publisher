"""文章 API"""
from flask import Blueprint, request, jsonify
from models import get_all_articles, get_article_by_id, create_article, update_article, delete_article

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles', methods=['GET'])
def list_articles():
    articles = get_all_articles()
    return jsonify([{
        'id': a.id, 'title': a.title, 'author': a.author, 'category': a.category,
        'summary': a.summary, 'status': a.status, 'source_file': a.source_file,
        'created_at': a.created_at.isoformat() if a.created_at else None,
        'updated_at': a.updated_at.isoformat() if a.updated_at else None,
    } for a in articles])

@articles_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': '文章不存在'}), 404
    return jsonify({
        'id': article.id, 'title': article.title, 'author': article.author,
        'category': article.category, 'summary': article.summary, 'content': article.content,
        'cover_image': article.cover_image, 'status': article.status, 'source_file': article.source_file,
        'created_at': article.created_at.isoformat() if article.created_at else None,
        'updated_at': article.updated_at.isoformat() if article.updated_at else None,
    })

@articles_bp.route('/articles', methods=['POST'])
def add_article():
    data = request.json
    article = create_article(data)
    return jsonify({'id': article.id, 'message': '文章创建成功'})

@articles_bp.route('/articles/<int:article_id>', methods=['PUT'])
def edit_article(article_id):
    data = request.json
    article = update_article(article_id, data)
    if not article:
        return jsonify({'error': '文章不存在'}), 404
    return jsonify({'message': '文章更新成功'})

@articles_bp.route('/articles/<int:article_id>', methods=['DELETE'])
def remove_article(article_id):
    delete_article(article_id)
    return jsonify({'message': '文章删除成功'})
