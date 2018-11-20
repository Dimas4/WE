from app.exceptions.exceptions import DomainNotFoundError, DomainRegexError, DomainError
from app.backend.domain import Domain


class Service:
    def __init__(self, url):
        self.domain = Domain(url)

    def check_domain(self):
        try:
            self.domain.check_domain()
        except (DomainNotFoundError, DomainRegexError):
            raise DomainError
