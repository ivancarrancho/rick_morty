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


app = Flask(__name__)


@app.route("/get_character", defaults={'character_id': None})
@app.route("/get_character/<int:character_id>")
def hello(character_id):
    data = request.get_json()
    filter = data.get("filter")
    is_zip_required = data.get("zip_required", False)

    filer_value = ""
    if filter:
        filer_value = filter

    path = f"https://rickandmortyapi.com/api/{filer_value}"
    if character_id or character_id == 0:
        path += f"/{character_id}"

    try:
        response = requests.get(path)
        json_response = validate_response(response)

        if json_response.get("error") or response.status_code != 200:
            raise Exception(json_response.get("error"))

        if is_zip_required:
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                file_name = f"{filer_value}.json"
                data = zipfile.ZipInfo(file_name)
                data.date_time = time.localtime(time.time())[:6]
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, response.content)

            memory_file.seek(0)
            return send_file(memory_file, attachment_filename=f"{filer_value}.zip", as_attachment=True)

        return json_response

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
