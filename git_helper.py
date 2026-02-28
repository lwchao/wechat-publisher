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
