from flask_classy import FlaskView

from app.exceptions.exceptions import DomainRegexError
from utils.response.response import Response
from app.service.service import Service


response = Response()


class BaseView(FlaskView):
    route_base = '/api/getemail/'

    def get(self, url):
        service = Service(url)
        try:
            service.check_domain()
        except DomainRegexError:
            return response.response_400()
