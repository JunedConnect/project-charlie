from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import os


# Celery Configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_journal.settings')
app = Celery('digital_journal')
app.conf.enable_utc = True
app.config_from_object(settings, namespace='CELERY')

# Update Celery configuration to accept JSON content
app.conf.update(
    accept_content=['json'],  # Allow JSON content
    task_serializer='json',
    result_serializer='json',
)

# Celery Beat Settings
app.conf.beat_schedule = {
    'send_reminder_email_daily_at_8pm_utc': {
        'task': 'journals.tasks.send_reminder_emails',
        'schedule': crontab(hour=20, minute=00),  # Runs every day at 20:00 UTC
    },
}

# Automatically discover tasks in all registered Django app configs
app.autodiscover_tasks()

# Debug settings
#@app.task(bind=True)
#def debug_task(self):
#    print(f'Request: {self.request!r}')