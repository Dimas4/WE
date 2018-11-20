import re

import requests

from app.exceptions.exceptions import DomainRegexError, DomainNotFoundError


class Domain:
    def __init__(self, url):
        self._url = url

        self.regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        self.domain = self._url.split('/')[2]  # TODO add method to get domain

    def _make_request(self, url):
        try:
            return requests.get(url, timeout=2)
        except requests.exceptions.ConnectionError:
            raise DomainNotFoundError

    def check_regex(self):
        url = re.match(self.regex, self._url)
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
