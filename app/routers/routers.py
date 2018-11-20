import json
import uuid

from flask import jsonify, request

from flask_classy import FlaskView

from app.exceptions.exceptions import DomainError
from app.service.domain.service import Service as Service_Domain
from app.service.database.service import Service as Service_DB

from utils.celery.celery import start_search
from utils.response.response import Response


response = Response()


class BaseView(FlaskView):
    route_base = '/api/getemail/'

    def get(self, token):
        result = Service_DB.get_one_by_token(token=token)
        if result:
            return result.answer
        return response.response_404()

    def post(self):
        data_json = json.loads(request.data)
        url = data_json.get('url')
        if url is None:
            return response.response_400()

        service = Service_Domain(url)
        try:
            service.check_domain()
        except DomainError:
            return response.response_400()

        _token = uuid.uuid4()
        start_search.delay(url, _token)

        return jsonify({'token': _token})
