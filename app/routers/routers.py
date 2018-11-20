import json
import uuid

from flask import jsonify, request

from flask_classy import FlaskView

from app.exceptions.exceptions import DomainError
from utils.celery.celery import start_search
from app.database.model import EmailsS, db
from utils.response.response import Response
from app.service.service import Service


response = Response()


class BaseView(FlaskView):
    route_base = '/api/getemail/'

    def get(self, token):
        result = EmailsS.get_one_by_token(token=token)
        if result:
            return result.answer
        return response.response_404()

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

        _token = uuid.uuid4()
        start_search.delay(url, _token)

        return jsonify({'token': _token})
