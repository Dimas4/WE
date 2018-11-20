from app.database.model import EmailsS


class Service:
    table = EmailsS

    @classmethod
    def get_one_by_token(cls, token):
        return cls.table.get_one_by_token(token=token)
