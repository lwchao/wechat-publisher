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
