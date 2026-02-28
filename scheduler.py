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
