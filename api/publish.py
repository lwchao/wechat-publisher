"""发布 API"""
import os
import yaml
import requests
import json
import re
import base64
from flask import Blueprint, request, jsonify
from models import get_article_by_id, create_publish_log, update_article, get_publish_logs
from git_helper import GitHelper

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


# 内嵌的蓝色封面图片 (100x100 JPEG)
DEFAULT_COVER_BASE64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCABkAGQDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDxyiiiv3E8wKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//Z"
DEFAULT_COVER_BASE64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAn/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCwAB//2Q=="


def upload_cover(access_token):
    """上传封面图片"""
    try:
        # 读取本地封面图片
        cover_path = os.path.join(os.path.dirname(__file__), 'cover.jpg')
        with open(cover_path, 'rb') as f:
            img_data = f.read()
        
        # 上传到微信
        upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
        files = {'media': ('cover.jpg', img_data, 'image/jpeg')}
        resp = requests.post(upload_url, files=files, timeout=30).json()
        
        if 'media_id' in resp:
            return resp['media_id']
        raise Exception(f"上传封面失败: {resp}")
    except Exception as e:
        raise Exception(f"上传封面失败: {e}")
    """上传一个简单的封面图片"""
    try:
        img_data = base64.b64decode(DEFAULT_COVER_BASE64)
        
        # 上传到微信
        upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
        files = {'media': ('cover.jpg', img_data, 'image/jpeg')}
        resp = requests.post(upload_url, files=files, timeout=30).json()
        
        if 'media_id' in resp:
            return resp['media_id']
        raise Exception(f"上传封面失败: {resp}")
    except Exception as e:
        raise Exception(f"上传封面失败: {e}")


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
    access_token = get_access_token(appid, secret)
    content_html = markdown_to_wechat(article['content'])
    
    # 上传封面
    thumb_media_id = upload_cover(access_token)
    
    article_data = {
        "title": article['title'][:20], 
        "author": article.get('author', '匿名')[:5],
        "content": content_html[:20000], 
        "digest": article.get('summary', '')[:20],
        "content_source_url": "", 
        "thumb_media_id": thumb_media_id,
        "pic_crop_235_1": "0_0_1_1", 
        "pic_crop_1_1": "0_0_1_1"
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    resp = requests.post(url, json={"articles": [article_data]}).json()
    
    if "media_id" not in resp:
        err_msg = resp.get('errmsg', str(resp))
        raise Exception(f"创建草稿失败: {err_msg}")
    
    media_id = resp["media_id"]
    
    if not draft_mode:
        publish_url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
        pub_resp = requests.post(publish_url, json={"media_id": media_id}).json()
        if pub_resp.get('errcode', 0) != 0:
            raise Exception(f"发布失败: {pub_resp.get('errmsg', str(pub_resp))}")
    
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
            'title': article.title, 
            'author': article.author, 
            'summary': article.summary,
            'content': article.content, 
            'cover_media_id': article.cover_image,
        }, draft_mode)
        
        create_publish_log(article_id, 'draft' if draft_mode else 'publish', media_id, '成功')
        update_article(article_id, {'status': 'published'})
        
        # 自动提交 GitHub
        config = load_config()
        if config.get('git', {}).get('auto_commit', False):
            try:
                git = GitHelper()
                import datetime
                commit_msg = config.get('git', {}).get('commit_message_template', 'Update: {date}').format(
                    date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                )
                result = git.auto_commit(commit_msg)
                if result.get('success') and config.get('git', {}).get('auto_push', False):
                    git.push()
            except Exception as e:
                print(f"自动提交失败: {e}")
        
        return jsonify({'message': '发布成功', 'media_id': media_id})
    
    except Exception as e:
        create_publish_log(article_id, 'draft', '', str(e))
        return jsonify({'error': str(e)}), 500


@publish_bp.route('/publish/logs', methods=['GET'])
def get_logs():
    logs = get_publish_logs()
    return jsonify([{
        'id': log.id, 
        'article_id': log.article_id, 
        'mode': log.mode,
        'wechat_media_id': log.wechat_media_id, 
        'result': log.result,
        'published_at': log.published_at.isoformat() if log.published_at else None,
    } for log in logs])
