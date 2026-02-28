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
