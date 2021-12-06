import requests
import json

from flask import Flask
from flask import request
from flask import Response

from format_checker import validate_response
from zip_creator import create_zip


app = Flask(__name__)


@app.route("/get_character", defaults={'character_id': None})
@app.route("/get_character/<int:character_id>")
def hello(character_id):
    data = request.get_json()
    filter = data.get("filter", "")
    is_zip_required = data.get("zip_required", False)

    path = f"https://rickandmortyapi.com/api/{filter}"
    if character_id or character_id == 0:
        path += f"/{character_id}"

    try:
        response = requests.get(path)

        json_response = validate_response(response)
    
        if json_response.get("error") or response.status_code != 200:
            raise Exception(json_response.get("error"))
    
        if is_zip_required:
            return create_zip(response=response, filter_value=filter)
    
        return json_response

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
