import requests
import json

from flask import Flask
from flask import request
from flask import Response

from flask_restx import Api, Resource

from format_checker import validate_response
from zip_creator import create_zip
from response_encoder import encode_response, decode_response


flask_app = Flask(__name__)
app = Api(app=flask_app)
name_space = app.namespace('swagger', description='Main APIs')


@name_space.route("/")
class MainClass(Resource):
    def get(self):
        return "<p>Go to postman!</p>"

    def post(self):
        return {
            "status": "Posted new data"
        }


@name_space.route("/decode")
class Decode(Resource):
    def get(self):
        data = request.get_json()
        response = data.get("response", "")
        email = data.get("email", "")
        return decode_response(response=response, email=email)


@name_space.route("/data-api", defaults={'data_id': None, 'data_type': None})
@name_space.route("/data-api/<string:data_type>", defaults={'data_id': None})
@name_space.route("/data-api/<string:data_type>/<int:data_id>")
class GetData(Resource):
    def get(self, data_type, data_id):
        try:
            data = request.get_json()
            email = data.get("email", "")
            is_zip_required = data.get("zip_required", False)
            is_encoded_response = data.get("encoded", False)
            format = "json"

            path = f"https://rickandmortyapi.com/api/{data_type}"
            if data_id or data_id == 0:
                path += f"/{data_id}"

            response = requests.get(path)

            final_response = validate_response(response)

            if final_response.get("error") or response.status_code != 200:
                raise Exception(final_response.get("error"))

            if is_encoded_response:
                final_response = encode_response(response=final_response, email=email)
                format = "txt"

            if is_zip_required:
                return create_zip(
                    response=final_response, filter_value=data_type, format=format
                )

            return final_response

        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
