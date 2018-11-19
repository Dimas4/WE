from flask import Flask


def create():
    return Flask(__name__)


app = create()
