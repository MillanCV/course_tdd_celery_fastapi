from celery import Celery
from project.app import create_app

app = create_app()
celery = app.celery_app



