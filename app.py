import requests
import json

from flask import Flask
from flask import request
from flask import Response

from format_checker import validate_response
from zip_creator import create_zip
from response_encoder import encode_response, decode_response


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Go to postman!</p>"


@app.route("/decode")
def decode():
    data = request.get_json()
    response = data.get("response", "")
    user_email = data.get("user_email", "")
    return decode_response(response=response, user_email=user_email)


@app.route("/get_character", defaults={'character_id': None})
@app.route("/get_character/<int:character_id>")
def hello(character_id):

    # try:
    data = request.get_json()
    filter = data.get("filter", "")
    email = data.get("email", "")
    is_zip_required = data.get("zip_required", False)
    is_encoded_response = data.get("encoded", False)
    format = "json"

    path = f"https://rickandmortyapi.com/api/{filter}"
    if character_id or character_id == 0:
        path += f"/{character_id}"

    response = requests.get(path)

    final_response = validate_response(response)

    if final_response.get("error") or response.status_code != 200:
        raise Exception(final_response.get("error"))

    if is_encoded_response:
        final_response = encode_response(response=final_response, user_email=email)
        format = "txt"

    if is_zip_required:
        return create_zip(response=final_response, filter_value=filter, format=format)

    return final_response

    # except Exception as e:
    #     return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
