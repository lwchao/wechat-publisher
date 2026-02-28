#!/usr/bin/env python3
"""Flask Web 应用主入口"""
import os
import yaml
from flask import Flask, render_template, jsonify
from flask_cors import CORS

def load_config():
    config_path = os.environ.get('CONFIG_PATH', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
CORS(app)
app.config['CONFIG'] = load_config()

# 注册蓝图
from api.articles import articles_bp
from api.publish import publish_bp
from api.git_ops import git_bp
from api.ai_gen import ai_bp
from api.webhook import webhook_bp
from api.scheduler import scheduler_bp
from api.config import config_bp

app.register_blueprint(articles_bp, url_prefix='/api')
app.register_blueprint(publish_bp, url_prefix='/api')
app.register_blueprint(git_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(webhook_bp, url_prefix='/api')
app.register_blueprint(scheduler_bp, url_prefix='/api')
app.register_blueprint(config_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/articles/new')
def article_new():
    return render_template('article_edit.html')

@app.route('/articles/<int:article_id>')
def article_edit(article_id):
    return render_template('article_edit.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/git')
def git_page():
    return render_template('git.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
