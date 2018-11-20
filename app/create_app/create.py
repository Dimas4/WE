from flask import Flask


def create():
    return Flask(__name__)


app = create()
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

