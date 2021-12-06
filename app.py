import requests
import json
import gzip
import zipfile
import io
import time

from flask import Flask
from flask import request
from flask import Response
from flask import make_response
from flask import send_file

from format_checker import validate_response

# from exceptions import ConflictExceptions
#
#
# from werkzeug.exceptions import (
#     BadRequest,
#     Forbidden,
#     InternalServerError,
#     NotFound,
#     Unauthorized,
#     Conflict,
# )

app = Flask(__name__)


@app.route("/get_character")
def hello():
    data = request.get_json()
    filter = data.get("filter")

    filer_value = ""
    if filter:
        filer_value = filter

    path = f"https://rickandmortyapi.com/api/{filer_value}"

    try:
        json_response = requests.get(path)

        if json_response.get("error") or response.status_code != 200:
            raise Exception(json_response.get("error"))

        return json_response

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
