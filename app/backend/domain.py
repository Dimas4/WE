import re

import requests

from app.exceptions.exceptions import DomainRegexError, DomainNotFoundError


class Domain:
    def __init__(self, domain, regex=None, security=None):
        self.domain = domain
        self.regex = r'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,4})*$'
        self.security = "http"
        self._url = f"{self.security}://{self.domain}"

    def _make_request(self, url):
        return requests.get(url)

    def check_regex(self):
        url = re.search(self.regex, self.domain)
        if url:
            return url.group(0)
        raise DomainRegexError

    def check_request(self):
        request = self._make_request(self._url)
        status = request.status_code
        if status >= 400:
            raise DomainNotFoundError

    def check_domain(self):
        self.check_regex()
        self.check_request()
