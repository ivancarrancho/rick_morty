import json


def validate_response(response):
    try:
        response_json = response.json()
        json.loads(response_json)

        return response_json

    except Exception:
        raise
