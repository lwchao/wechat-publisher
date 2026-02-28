# 微信公众号发布工具扩展实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为微信公众号发布工具增加 Web 界面、GitHub 集成、AI 生成文章功能

**Architecture:** Flask + SQLite + 原生前端，实现轻量级 Web 服务

**Tech Stack:** Flask, SQLAlchemy, SQLite, Tailwind CSS

---

## 任务总览

| 阶段 | 任务数 | 说明 |
|------|--------|------|
| 阶段1 | 5 | 基础设施搭建 |
| 阶段2 | 4 | 数据库模型 |
| 阶段3 | 6 | 核心 API |
| 阶段4 | 5 | Git 操作 |
| 阶段5 | 4 | AI 生成 |
| 阶段6 | 3 | Webhook |
| 阶段7 | 3 | 定时任务 |
| 阶段8 | 5 | Web 界面 |
| **总计** | **35** | |

---

## 阶段1: 基础设施搭建

### Task 1: 更新依赖文件

**Files:**
- Modify: `requirements.txt`

```txt
flask>=2.3.0
flask-cors>=4.0.0
sqlalchemy>=2.0.0
requests>=2.28.0
python-frontmatter>=1.0.0
pyyaml>=6.0
apscheduler>=8.0.0
```

### Task 2: 创建 Flask 主应用

**Files:**
- Create: `app.py`

```python
#!/usr/bin/env python3
"""Flask Web 应用主入口"""
import os
import yaml
from flask import Flask, render_template
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
    return render_template('article_edit.html', article_id=article_id)

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/git')
def git_page():
    return render_template('git.html')

@app.route('/api/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### Task 3: 创建目录和空包

**Files:**
- Create: `api/__init__.py`
- Create: `templates/.gitkeep`
- Create: `static/.gitkeep`

### Task 4: 创建 requirements.txt 并安装

**Files:**
- Modify: `requirements.txt`

```txt
flask>=2.3.0
flask-cors>=4.0.0
sqlalchemy>=2.0.0
requests>=2.28.0
python-frontmatter>=1.0.0
pyyaml>=6.0
apscheduler>=8.0.0
```

Run: `pip install -r requirements.txt`

### Task 5: 测试 Flask 启动

Run: `python -c "from app import app; print('OK')"`

---

## 阶段2: 数据库模型

### Task 6: 创建数据库模块

**Files:**
- Create: `database.py`

```python
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
```

Run: `python -c "from database import init_db; init_db(); print('DB init OK')"`

### Task 7: 创建数据模型操作

**Files:**
- Create: `models.py`

```python
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
```

---

## 阶段3: 核心 API

### Task 8: 文章 API

**Files:**
- Create: `api/articles.py`

```python
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
```

### Task 9: 发布 API

**Files:**
- Create: `api/publish.py`

```python
"""发布 API"""
import os, yaml, requests, json, re
from flask import Blueprint, request, jsonify
from models import get_article_by_id, create_publish_log, update_article

publish_bp = Blueprint('publish', __name__)

def load_config():
    with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def get_access_token(appid, secret):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    resp = requests.get(url, params={"grant_type": "client_credential", "appid": appid, "secret": secret}).json()
    if "access_token" in resp:
        return resp["access_token"]
    raise Exception(f"获取token失败: {resp}")

def markdown_to_wechat(md_content):
    html = md_content
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre>\2</pre>', html, flags=re.DOTALL)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', html)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = html.replace("\n\n", "</p><p>")
    return f"<p>{html}</p>"

def publish_to_wechat(article, draft_mode=True):
    config = load_config()
    appid, secret = config.get('wechat', {}).get('appid'), config.get('wechat', {}).get('secret')
    default_cover = config.get('wechat', {}).get('default_cover_media_id')
    access_token = get_access_token(appid, secret)
    content_html = markdown_to_wechat(article['content'])
    thumb_media_id = article.get('cover_media_id') or default_cover
    article_data = {
        "title": article['title'][:20], "author": article.get('author', '匿名')[:5],
        "content": content_html[:20000], "digest": article.get('summary', '')[:20],
        "content_source_url": "", "thumb_media_id": thumb_media_id,
        "pic_crop_235_1": "0_0_1_1", "pic_crop_1_1": "0_0_1_1"
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    resp = requests.post(url, data=json.dumps({"articles": [article_data]}, ensure_ascii=False).encode('utf-8'),
                         headers={'Content-Type': 'application/json; charset=utf-8'}).json()
    if "media_id" not in resp:
        raise Exception(f"创建草稿失败: {resp}")
    media_id = resp["media_id"]
    if not draft_mode:
        publish_url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
        requests.post(publish_url, json={"media_id": media_id}).json()
    return media_id

@publish_bp.route('/publish', methods=['POST'])
def publish():
    data = request.json
    article_id = data.get('article_id')
    draft_mode = data.get('draft_mode', True)
    article = get_article_by_id(article_id)
    if not article:
        return jsonify({'error': '文章不存在'}), 404
    try:
        media_id = publish_to_wechat({
            'title': article.title, 'author': article.author, 'summary': article.summary,
            'content': article.content, 'cover_media_id': article.cover_image,
        }, draft_mode)
        create_publish_log(article_id, 'draft' if draft_mode else 'publish', media_id, '成功')
        update_article(article_id, {'status': 'published'})
        return jsonify({'message': '发布成功', 'media_id': media_id})
    except Exception as e:
        create_publish_log(article_id, 'draft', '', str(e))
        return jsonify({'error': str(e)}), 500

@publish_bp.route('/publish/logs', methods=['GET'])
def get_logs():
    logs = get_publish_logs()
    return jsonify([{
        'id': log.id, 'article_id': log.article_id, 'mode': log.mode,
        'wechat_media_id': log.wechat_media_id, 'result': log.result,
        'published_at': log.published_at.isoformat() if log.published_at else None,
    } for log in logs])
```

### Task 10: 配置 API

**Files:**
- Create: `api/config.py`

```python
"""配置 API"""
import os, yaml
from flask import Blueprint, request, jsonify

config_bp = Blueprint('config', __name__)

def load_config():
    with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'w') as f:
        yaml.dump(config, f, allow_unicode=True)

@config_bp.route('/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@config_bp.route('/config', methods=['PUT'])
def update_config():
    data = request.json
    config = load_config()
    config.update(data)
    save_config(config)
    return jsonify({'message': '配置更新成功'})
```

---

## 阶段4: Git 操作

### Task 11: Git 辅助模块

**Files:**
- Create: `git_helper.py`

```python
"""Git 操作辅助模块"""
import subprocess
from pathlib import Path

class GitHelper:
    def __init__(self, repo_path='.'):
        self.repo_path = Path(repo_path)
    
    def run(self, *args):
        result = subprocess.run(['git'] + list(args), cwd=self.repo_path, capture_output=True, text=True)
        return result
    
    def status(self):
        result = self.run('status', '--porcelain')
        if result.returncode != 0:
            return {'error': result.stderr}
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        files = [{'status': line[:2], 'file': line[3:]} for line in lines if len(line) >= 3]
        return {'clean': len(files) == 0, 'files': files}
    
    def add(self, *files):
        result = self.run('add', *files) if files else self.run('add', '.')
        return {'success': result.returncode == 0, 'output': result.stdout, 'error': result.stderr}
    
    def commit(self, message):
        result = self.run('commit', '-m', message)
        return {'success': result.returncode == 0, 'output': result.stdout, 'error': result.stderr}
    
    def push(self, remote='origin', branch=None):
        result = self.run('push', remote, branch) if branch else self.run('push', remote)
        return {'success': result.returncode == 0, 'output': result.stdout, 'error': result.stderr}
    
    def pull(self, remote='origin', branch=None):
        result = self.run('pull', remote, branch) if branch else self.run('pull', remote)
        return {'success': result.returncode == 0, 'output': result.stdout, 'error': result.stderr}
    
    def log(self, limit=10):
        result = self.run('log', f'-{limit}', '--oneline', '--pretty=format:%h|%s|%an|%ai')
        if result.returncode != 0:
            return {'error': result.stderr}
        return [{'hash': p[0], 'message': p[1], 'author': p[2], 'date': p[3]} 
                for line in result.stdout.strip().split('\n') if line and (p := line.split('|', 3))]
    
    def current_branch(self):
        result = self.run('branch', '--show-current')
        return result.stdout.strip() if result.returncode == 0 else None
    
    def auto_commit(self, message=None):
        status = self.status()
        if status.get('clean'):
            return {'success': True, 'message': '没有需要提交的更改'}
        self.add()
        import datetime
        message = message or f"Update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = self.commit(message)
        return {'success': result['success'], 'message': '提交成功' if result['success'] else result['error']}
```

### Task 12: Git API

**Files:**
- Create: `api/git_ops.py`

```python
"""Git 操作 API"""
from flask import Blueprint, request, jsonify
from git_helper import GitHelper

git_bp = Blueprint('git', __name__)

@git_bp.route('/git/status', methods=['GET'])
def get_status():
    git = GitHelper()
    status = git.status()
    status['branch'] = git.current_branch()
    return jsonify(status)

@git_bp.route('/git/add', methods=['POST'])
def git_add():
    data = request.json or {}
    files = data.get('files', [])
    git = GitHelper()
    result = git.add(*files) if files else git.add()
    return jsonify(result)

@git_bp.route('/git/commit', methods=['POST'])
def git_commit():
    data = request.json
    message = data.get('message', 'Update')
    git = GitHelper()
    return jsonify(git.commit(message))

@git_bp.route('/git/push', methods=['POST'])
def git_push():
    data = request.json or {}
    git = GitHelper()
    return jsonify(git.push(data.get('remote', 'origin'), data.get('branch')))

@git_bp.route('/git/log', methods=['GET'])
def get_log():
    limit = request.args.get('limit', 10, type=int)
    git = GitHelper()
    return jsonify(git.log(limit))
```

---

## 阶段5: AI 生成

### Task 13: AI 写作模块

**Files:**
- Create: `ai_writer.py`

```python
"""AI 写作模块"""
import os, json, requests
from typing import Optional, Dict

class AIWriter:
    SUPPORTED_MODELS = {'glm': '智谱 GLM', 'minimax': 'MiniMax', 'qwen': '通义千问'}
    
    def __init__(self, model: str = 'glm'):
        self.model = model
        import yaml
        with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'r') as f:
            self.config = yaml.safe_load(f).get('ai', {})
    
    def _get_api_key(self) -> str:
        model_config = self.config.get(self.model, {})
        return model_config.get('api_key') or os.environ.get(f'{self.model.upper()}_API_KEY')
    
    def _get_base_url(self) -> str:
        return self.config.get(self.model, {}).get('base_url', '')
    
    def generate(self, keyword: str, style: str = '技术文章', length: str = '中等', title: Optional[str] = None) -> str:
        if self.model == 'glm':
            return self._generate_glm(keyword, style, length, title)
        elif self.model == 'minimax':
            return self._generate_minimax(keyword, style, length, title)
        elif self.model == 'qwen':
            return self._generate_qwen(keyword, style, length, title)
        raise ValueError(f"不支持的模型: {self.model}")
    
    def _build_prompt(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        length_map = {'短': '500-800 字', '中等': '1000-1500 字', '长': '2000-3000 字'}
        return f"""请根据以下关键词生成一篇适合微信公众号发布的文章。

关键词: {keyword}
文章标题: {title or '请根据关键词生成'}
文章风格: {style}
文章长度: {length_map.get(length, '中等')}

要求:
1. 文章格式为 Markdown
2. 开头要有吸引人的引言
3. 结构清晰，有多个小标题
4. 内容专业但不晦涩
5. 适合手机阅读
6. 可以添加适度的表情符号增加趣味性

请生成完整的文章内容。"""
    
    def _generate_glm(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        api_key = self._get_api_key()
        base_url = self._get_base_url() or 'https://open.bigmodel.cn/api/paas/v4'
        prompt = self._build_prompt(keyword, style, length, title)
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'glm-4', 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.7}
        resp = requests.post(f'{base_url}/chat/completions', headers=headers, json=data, timeout=120)
        if resp.status_code != 200:
            raise Exception(f"API 调用失败: {resp.text}")
        return resp.json()['choices'][0]['message']['content']
    
    def _generate_minimax(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        api_key = self._get_api_key()
        base_url = self._get_base_url() or 'https://api.minimax.chat/v1'
        prompt = self._build_prompt(keyword, style, length, title)
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'abab6.5s-chat', 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.7}
        resp = requests.post(f'{base_url}/text/chatcompletion_v2', headers=headers, json=data, timeout=120)
        if resp.status_code != 200:
            raise Exception(f"API 调用失败: {resp.text}")
        return resp.json()['choices'][0]['message']['content']
    
    def _generate_qwen(self, keyword: str, style: str, length: str, title: Optional[str]) -> str:
        api_key = self._get_api_key()
        base_url = self._get_base_url() or 'https://dashscope.aliyuncs.com/api/v1'
        prompt = self._build_prompt(keyword, style, length, title)
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        data = {'model': 'qwen-turbo', 'input': {'messages': [{'role': 'user', 'content': prompt}]}, 'parameters': {'temperature': 0.7}}
        resp = requests.post(f'{base_url}/services/aigc/text-generation/generation', headers=headers, json=data, timeout=120)
        if resp.status_code != 200:
            raise Exception(f"API 调用失败: {resp.text}")
        return resp.json()['output']['text']
```

### Task 14: AI API

**Files:**
- Create: `api/ai_gen.py`

```python
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
```

---

## 阶段6: Webhook

### Task 15: GitHub Webhook

**Files:**
- Create: `api/webhook.py`

```python
"""GitHub Webhook API"""
import hmac, hashlib, json
from flask import Blueprint, request, jsonify
from git_helper import GitHelper

webhook_bp = Blueprint('webhook', __name__)

def verify_signature(payload, signature, secret):
    if not signature or not secret:
        return True
    expected = 'sha256=' + hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

@webhook_bp.route('/webhook/github', methods=['POST'])
def github_webhook():
    import os, yaml
    with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    secret = config.get('webhook', {}).get('github_secret', '')
    
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature, secret):
        return jsonify({'error': '签名验证失败'}), 401
    
    event = request.headers.get('X-GitHub-Event', 'push')
    payload = request.json
    
    if event == 'push':
        commits = payload.get('commits', [])
        articles_changed = any('articles/' in c.get('modified', []) for c in commits)
        return jsonify({'message': 'Push 收到', 'articles_changed': articles_changed})
    
    return jsonify({'message': '事件已接收', 'event': event})
```

---

## 阶段7: 定时任务

### Task 16: 定时任务模块

**Files:**
- Create: `scheduler.py`

```python
"""定时任务模块"""
import os, yaml
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from pathlib import Path

class PublishScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        with open(os.environ.get('CONFIG_PATH', 'config.yaml'), 'r') as f:
            self.config = yaml.safe_load(f)
        self.enabled = self.config.get('schedule', {}).get('enabled', False)
    
    def check_and_publish(self):
        articles_dir = self.config.get('articles_dir', './articles')
        path = Path(articles_dir)
        if not path.exists():
            return
        md_files = list(path.glob('*.md'))
        print(f"Found {len(md_files)} articles")
    
    def start(self):
        if not self.enabled:
            print("Scheduler is disabled")
            return
        schedule_config = self.config.get('schedule', {})
        mode = schedule_config.get('mode', 'cron')
        
        if mode == 'cron':
            cron = schedule_config.get('cron', '0 9 * * *')
            trigger = CronTrigger.from_crontab(cron)
        else:
            minutes = schedule_config.get('interval_minutes', 30)
            trigger = IntervalTrigger(minutes=minutes)
        
        self.scheduler.add_job(self.check_and_publish, trigger, id='publish_check')
        self.scheduler.start()
        print(f"Scheduler started: {mode} mode")
    
    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
    
    def status(self):
        return {
            'enabled': self.enabled,
            'running': self.scheduler.running,
            'jobs': [{'id': j.id, 'next_run': str(j.next_run_time)} for j in self.scheduler.get_jobs()]
        }
```

### Task 17: 定时任务 API

**Files:**
- Create: `api/scheduler.py`

```python
"""定时任务 API"""
from flask import Blueprint, jsonify
from scheduler import PublishScheduler

scheduler_bp = Blueprint('scheduler', __name__)
scheduler = PublishScheduler()

@scheduler_bp.route('/scheduler/status', methods=['GET'])
def get_status():
    return jsonify(scheduler.status())

@scheduler_bp.route('/scheduler/start', methods=['POST'])
def start_scheduler():
    scheduler.start()
    return jsonify({'message': '定时任务已启动'})

@scheduler_bp.route('/scheduler/stop', methods=['POST'])
def stop_scheduler():
    scheduler.stop()
    return jsonify({'message': '定时任务已停止'})
```

---

## 阶段8: Web 界面

### Task 18: 基础模板和页面

**Files:**
- Create: `templates/base.html`
- Create: `templates/index.html`
- Create: `templates/articles.html`
- Create: `templates/article_edit.html`
- Create: `templates/generate.html`
- Create: `templates/git.html`
- Create: `static/style.css`

由于篇幅限制，HTML 模板请参考详细设计文档。

---

## Task 19: 更新配置

**Files:**
- Modify: `config.yaml`

```yaml
ai:
  default_model: glm
  glm:
    api_key: ""
    base_url: ""
  minimax:
    api_key: ""
    base_url: ""
  qwen:
    api_key: ""
    base_url: ""

webhook:
  enabled: true
  github_secret: ""
  auto_publish_on_push: false

schedule:
  enabled: false
  mode: cron
  cron: "0 9 * * *"
  delay_minutes: 30

git:
  auto_commit: false
  auto_push: false
```

---

## 执行方式选择

**Plan complete.**

### 两个执行选项：

1. **Subagent-Driven (本会话)** - 每完成一个任务后进行代码审查，快速迭代

2. **Parallel Session (新会话)** - 在新会话中批量执行，有检查点

请选择你希望的执行方式？
