from celery import Celery
from project import create_app

app = create_app()

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)


@app.get('/')
async def root():
    return {"message": "hello"}


@celery.task
def divide(x: int, y: int):
    import time
    time.sleep(5)
    return x/ y
    