from flask import Response as Response_Flask


class Response:
    def response_400(self):
        return Response_Flask(status=400)

    def response_404(self):
        return Response_Flask("Nor found", status=404)
