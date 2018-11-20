import pathlib

from app.create_app.create import app

from flask_sqlalchemy import SQLAlchemy


path = pathlib.Path(__file__).parent.parent.parent

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].format(path=path)

db = SQLAlchemy(app)


class EmailsS(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    answer = db.Column(db.String(500), nullable=False)

    @classmethod
    def get_one_by_token(cls, token):
        return db.session.query(cls).filter_by(token=token).first()

    def __repr__(self):
        return '<Emails %r>' % self.answer
