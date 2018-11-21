from app.database.model import Emails


class Service:
    table = Emails

    @classmethod
    def get_one_by_token(cls, token):
        return cls.table.get_one_by_token(token=token)

    @classmethod
    def get_all(cls):
        return cls.table.get_all()

