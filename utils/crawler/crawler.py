import re

import requests

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url):
        self._url = url

        self._base_url = self._get_base(self._url)

        self._emails = {}
        self._erros = []

    def _get_base(self, url):
        return '/'.join(url.split('/')[:3])

    def _make_request(self, url):
        return requests.get(url, timeout=5)

    def _get_html(self, url):
        request = self._make_request(url)
        return request.text

    def _create_soup(self, html, mode="html.parser"):
        return BeautifulSoup(html, mode)

    def _find_a_tag(self, html, mode="html.parser"):
        soup = self._create_soup(html, mode)
        return soup.find_all('a')

    def _get_hrefs(self, a_tags):
        return [tag.get('href') for tag in a_tags]

    def _find_email(self, html):
        return set(re.findall(r'[\w\.-]+@[\w\.-]+', html))

    def _clear_urls(self, urls):
        _urls = []
        for url in urls:
            if url is not None:
                _urls.append(url)
        return _urls

    def _check_and_get_urls(self, urls):
        for ind, url in enumerate(urls):
            try:
                if 'http' not in url:
                    urls[ind] = f"{self._base_url}{url}"
            except Exception as err:
                pass
        return urls

    def search(self):
        html = self._get_html(self._url)
        a_tags = self._find_a_tag(html)
        urls = self._get_hrefs(a_tags)
        urls = self._check_and_get_urls(urls)
        urls = self._clear_urls(urls)
        from tqdm import tqdm

        for url in tqdm(urls):
            try:
                html = self._get_html(url)
                emails = self._find_email(html)
                self._emails[url] = tuple(emails)
            except (requests.exceptions.InvalidURL, requests.exceptions.ConnectionError):
                self._erros.append(url)

        return {'data': self._emails, 'errors': self._erros}
