"""AI 生成 API"""
import re
from flask import Blueprint, request, jsonify
from ai_writer import AIWriter
from models import create_article

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/models', methods=['GET'])
def get_models():
    return jsonify(AIWriter.SUPPORTED_MODELS)

@ai_bp.route('/ai/generate', methods=['POST'])
def generate_article():
    data = request.json
    keyword = data.get('keyword')
    model = data.get('model', 'glm')
    style = data.get('style', '技术文章')
    length = data.get('length', '中等')
    title = data.get('title')
    
    if not keyword:
        return jsonify({'error': '请提供关键词'}), 400
    
    try:
        writer = AIWriter(model)
        content = writer.generate(keyword, style, length, title)
        return jsonify({'content': content, 'keyword': keyword, 'model': model})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/save', methods=['POST'])
def save_article():
    data = request.json
    content = data.get('content')
    keyword = data.get('keyword', '')
    title = data.get('title')
    
    if not content:
        return jsonify({'error': '请提供文章内容'}), 400
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    
    article = create_article({
        'title': title or keyword or 'AI 生成文章',
        'content': content,
        'summary': content[:200] if content else '',
        'source_file': '',
    })
    return jsonify({'id': article.id, 'message': '文章保存成功'})
