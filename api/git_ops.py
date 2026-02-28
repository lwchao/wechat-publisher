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
