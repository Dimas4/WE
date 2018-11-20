from flask import Flask

from config.get_config import get_config


def create():
    return Flask(__name__)


app = create()

config = get_config()

app.config.update(**config['database'], **config['celery'])
