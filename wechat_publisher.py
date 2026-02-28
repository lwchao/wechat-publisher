#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
import requests
import frontmatter
import yaml
from pathlib import Path
from datetime import datetime

CONFIG_PATH = "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_access_token(appid, secret):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {"grant_type": "client_credential", "appid": appid, "secret": secret}
    resp = requests.get(url, params=params).json()
    if "access_token" in resp:
        return resp["access_token"]
    else:
        raise Exception(f"获取token失败: {resp}")

def get_latest_article(articles_dir):
    md_files = list(Path(articles_dir).glob("*.md"))
    if not md_files:
        return None
    return max(md_files, key=os.path.getmtime)

def parse_markdown(file_path):
    post = frontmatter.load(file_path)
    return {
        "title": post.metadata.get("title", "无标题"),
        "author": post.metadata.get("author", "匿名"),
        "category": post.metadata.get("category", "未分类"),
        "summary": post.metadata.get("summary", ""),
        "cover_image": post.metadata.get("cover_image", ""),
        "draft": post.metadata.get("draft", True),
        "content": post.content,
    }

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
    html = f"<p>{html}</p>"
    
    return html

def upload_thumb(access_token, image_url):
    if not image_url:
        return None
    
    try:
        import ssl
        import io
        from urllib.request import urlopen, Request
        
        req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, context=ssl._create_unverified_context()) as response:
            image_data = response.read()
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
        files = {"media": ("cover.jpg", io.BytesIO(image_data), "image/jpeg")}
        resp = requests.post(url, files=files).json()
        return resp.get("media_id")
    except Exception as e:
        print(f"上传封面图片失败: {e}")
        return None

def create_draft(access_token, article, config):
    import json
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    thumb_media_id = article.get("cover_media_id") or config.get("wechat", {}).get("default_cover_media_id")
    
    content_html = markdown_to_wechat(article["content"])
    
    article_data = {
        "title": article["title"][:20],
        "author": article["author"][:5],
        "content": content_html[:20000],
        "digest": article.get("summary", "")[:20],
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "pic_crop_235_1": "0_0_1_1",
        "pic_crop_1_1": "0_0_1_1"
    }
    
    resp = requests.post(
        url, 
        data=json.dumps({"articles": [article_data]}, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'}
    ).json()
    
    if "media_id" in resp:
        return resp["media_id"]
    else:
        raise Exception(f"创建草稿失败: {resp}")

def publish_article(access_token, media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    data = {"media_id": media_id}
    resp = requests.post(url, json=data).json()
    
    if resp.get("errcode") == 0:
        return True
    else:
        raise Exception(f"发布失败: {resp}")

def main():
    parser = argparse.ArgumentParser(description="微信公众号自动发布工具")
    parser.add_argument("--file", "-f", help="指定要发布的Markdown文件")
    parser.add_argument("--publish", "-p", action="store_true", help="直接发布，不使用草稿模式")
    parser.add_argument("--config", "-c", default="config.yaml", help="配置文件路径")
    args = parser.parse_args()
    
    global CONFIG_PATH
    CONFIG_PATH = args.config
    
    config = load_config()
    
    articles_dir = config.get("articles_dir", "./articles")
    
    if args.file:
        file_path = Path(articles_dir) / args.file
    else:
        file_path = get_latest_article(articles_dir)
    
    if not file_path or not file_path.exists():
        print(f"没有找到可发布的文章: {articles_dir}")
        sys.exit(1)
    
    print(f"正在处理: {file_path}")
    
    article = parse_markdown(file_path)
    print(f"标题: {article['title']}")
    print(f"作者: {article['author']}")
    
    draft_mode = config.get("publish", {}).get("draft_mode", True)
    if args.publish:
        draft_mode = False
    
    print(f"发布模式: {'草稿' if draft_mode else '直接发布'}")
    
    appid = config.get("wechat", {}).get("appid")
    secret = config.get("wechat", {}).get("secret")
    
    if not appid or not secret:
        print("错误: 请在config.yaml中配置appid和secret")
        sys.exit(1)
    
    try:
        access_token = get_access_token(appid, secret)
        print("获取Access Token成功")
        
        media_id = create_draft(access_token, article, config)
        print(f"创建草稿成功, media_id: {media_id}")
        
        if not draft_mode:
            if publish_article(access_token, media_id):
                print("文章发布成功!")
        else:
            print("已保存到草稿箱，请登录微信公众号后台查看并发布")
            
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
