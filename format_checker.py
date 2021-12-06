import json


def validate_response(response):
    try:
        response_json = response.text
        response = json.loads(response_json)

        return response

    except Exception:
        raise