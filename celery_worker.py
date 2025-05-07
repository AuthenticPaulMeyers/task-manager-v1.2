from celery import Celery
from myapp import create_app

app = create_app()

celery = Celery(
    app.import_name,
    broker='redis://localhost:6379/0'
)
celery.conf.update(app.config)
