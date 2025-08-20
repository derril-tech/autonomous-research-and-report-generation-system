"""
Celery configuration for background task processing
"""

import os
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "research_system",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.research_tasks",
        "app.tasks.monitoring_tasks",
        "app.tasks.export_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_always_eager=False,  # Set to True for testing
    result_expires=3600,  # 1 hour
    result_persistent=True,
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 3600,
    },
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "monitor-topics": {
        "task": "app.tasks.monitoring_tasks.monitor_topics",
        "schedule": crontab(minute="*/30"),  # Every 30 minutes
    },
    "cleanup-old-jobs": {
        "task": "app.tasks.maintenance_tasks.cleanup_old_jobs",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    "update-job-statuses": {
        "task": "app.tasks.maintenance_tasks.update_stuck_jobs",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
}

# Task routing
celery_app.conf.task_routes = {
    "app.tasks.research_tasks.*": {"queue": "research"},
    "app.tasks.monitoring_tasks.*": {"queue": "monitoring"},
    "app.tasks.export_tasks.*": {"queue": "export"},
    "app.tasks.maintenance_tasks.*": {"queue": "maintenance"},
}

# Task annotations for specific task configurations
celery_app.conf.task_annotations = {
    "app.tasks.research_tasks.start_research_workflow": {
        "rate_limit": "10/m",  # 10 tasks per minute
        "time_limit": 7200,  # 2 hours
        "soft_time_limit": 3600,  # 1 hour
    },
    "app.tasks.export_tasks.generate_report": {
        "rate_limit": "30/m",  # 30 tasks per minute
        "time_limit": 1800,  # 30 minutes
        "soft_time_limit": 900,  # 15 minutes
    },
    "app.tasks.monitoring_tasks.monitor_topics": {
        "rate_limit": "2/m",  # 2 tasks per minute
        "time_limit": 3600,  # 1 hour
        "soft_time_limit": 1800,  # 30 minutes
    },
}

if __name__ == "__main__":
    celery_app.start()
