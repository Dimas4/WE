import json
import uuid

from flask import jsonify, request

from flask_classy import FlaskView

from app.exceptions.exceptions import DomainError
from app.backend.celery import start_search
from app.service.service import Service
from app.database.model import EmailsS, db
from utils.response.response import Response


response = Response()


class BaseView(FlaskView):
    route_base = '/api/getemail/'

    def get(self, token):
        result = db.session.query(EmailsS).filter_by(token=token).first()
        if result:
            return jsonify(result.answer)
        return jsonify({'answer': 'not found'})

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
