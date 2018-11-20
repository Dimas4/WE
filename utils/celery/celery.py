import json

from app.database.model import db, EmailsS
from utils.crawler.crawler import Crawler
from .create_celery import celery


@celery.task
def start_search(url, token):
    crawler = Crawler(url)
    answer = json.dumps(crawler.search())

    emails = EmailsS(token=token, answer=answer)
    db.session.add(emails)
    db.session.commit()
