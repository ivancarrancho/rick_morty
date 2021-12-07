import requests
import json

from flask import Flask
from flask import request
from flask import Response

from flask_restx import Api, Resource, fields

from format_checker import validate_response
from zip_creator import create_zip
from response_encoder import encode_response, decode_response


flask_app = Flask(__name__)
flask_app.url_map.strict_slashes = False
app = Api(
    app=flask_app,
    version="1.0",
    title="Rick & Morty App",
    description="Get multiple rick & morty data"
)

name_space = app.namespace('app', description='Rick & Morty APIs')


@name_space.route("/")
class MainClass(Resource):
    def get(self):
        return "Use postman please"


@name_space.route("/decode")
class Decode(Resource):
    model = app.model(
        'Data Model', {
            'email': fields.String(
                required=False,
                description="Email which was used in the encryption",
                help=""
            ),
            'response': fields.String(
                required=True,
                description="Send True to receive a .zip with the compressed data",
                help="Disable to receive a json or txt file"
            )
        }
    )

    @app.expect(model)
    def get(self):
        data = request.get_json() or {}
        response = data.get("response", "")
        email = data.get("email", "")

        return decode_response(response=response, email=email)


@name_space.route("/data-api", defaults={'data_id': None, 'data_type': ""})
@name_space.route("/data-api/<string:data_type>", defaults={'data_id': ""})
@name_space.route("/data-api/<string:data_type>/<int:data_id>")
class GetData(Resource):
    model = app.model(
        'Data Model', {
            'email': fields.String(
                required=False,
                description="Email to be used in the encryption",
                help=""
            ),
            'zip_required': fields.Boolean(
                required=True,
                description="Send True to receive a .zip with the compressed data",
                help="Disable to receive a json or txt file"
            ),
            'encoded': fields.Boolean(
                required=True,
                description="Send True to receive all the encoded data",
                help=""
            )
        }
    )

    @app.doc(
        params={
            'data_type': 'type of request Ie. character,location or episode',
            'data_id': 'String with the object id, null get all the request types',
        }
    )
    @app.expect(model)
    def get(self, data_type, data_id):
        try:
            data = request.get_json() or {}
            email = data.get("email", "")
            is_zip_required = data.get("zip_required", False)
            is_encoded_response = data.get("encoded", False)
            format = "json"

            path = f"https://rickandmortyapi.com/api/{data_type}"
            if data_id or data_id == 0:
                path += f"/{data_id}"

            print(f"Path: {path}")

            response = requests.get(path)
            final_response = validate_response(response)

            if final_response.get("error") or response.status_code != 200:
                raise Exception(final_response.get("error"))

            if is_encoded_response:
                final_response = encode_response(response=final_response, email=email)
                format = "txt"

            if is_zip_required:
                return create_zip(
                    response=str(final_response), filter_value=data_type, format=format
                )

            return final_response

        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
