import json

from flask import jsonify, request

from flask_classy import FlaskView

from app.exceptions.exceptions import DomainError
from app.backend.crawler import Crawler
from app.service.service import Service

from utils.response.response import Response


response = Response()


class BaseView(FlaskView):
    route_base = '/api/getemail/'

    def post(self):
        data_json = json.loads(request.data)
        url = data_json.get('url')
        if url is None:
            return response.response_400()

        service = Service(url)
        try:
            service.check_domain()
        except DomainError:
            return response.response_400()

        crawler = Crawler(url)
        result = crawler.search()
        return jsonify(result)
