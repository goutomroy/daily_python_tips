from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_python_tips.settings')


class Config:

    broker_url = 'redis://localhost:6379/2'
    result_backend = 'django-db'
    result_cache_max = 1000
    worker_concurrency = 8
    beat_max_loop_interval = 600
    task_compression = 'gzip'
    result_compression = 'gzip'
    task_default_queue = 'low'
    result_persistent = True
    task_track_started = True
    task_publish_retry = True
    task_publish_retry_policy = {
        'max_retries': 3,
        'interval_start': 0.2,
        'interval_step': 0.2,
        'interval_max': 1,
    }
    beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

    beat_schedule = {

        'data_builder': {
            'task': 'apps.warehouse.tasks.data_builder',
            'schedule': crontab(hour=11, minute=5),
        },

        'favourite_retweet_count_updater': {
            'task': 'apps.warehouse.tasks.favourite_retweet_count_updater',
            'schedule': crontab(hour=5, minute=5),
        },
    }

    task_queues = (

        Queue('low', Exchange('low'), routing_key='low'),
        Queue('high', Exchange('high'), routing_key='high')
    )

    task_routes = {

        'apps.warehouse.tasks.data_builder': 'high',
        'apps.warehouse.tasks.favourite_retweet_count_updater': 'low',
    }


celery_app = Celery('daily_python_tips')
celery_app.config_from_object(Config)
celery_app.autodiscover_tasks()
