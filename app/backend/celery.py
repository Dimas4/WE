from app.database.model import db, EmailsS
from app.backend.crawler import Crawler
from app.create_app.create import app
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)


@celery.task
def start_search(url, token):
    crawler = Crawler(url)
    answer = str(crawler.search())

    emails = EmailsS(token=token, answer=answer)
    db.session.add(emails)
    db.session.commit()
