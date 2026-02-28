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
