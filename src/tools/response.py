import json
from flask import Response

def make_json_response(status_code, message, data) -> Response:
    response_data = dict(
        code=status_code,
        message=message,
        data=data
    )

    return Response(
        response=json.dumps(response_data),
        status=status_code,
        mimetype="application/json"
    )

def make_otp_response_data(attempt):
    return dict(
        attempt=attempt
    )