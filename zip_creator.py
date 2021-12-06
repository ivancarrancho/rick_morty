import zipfile
import io
import time

from flask import send_file


def create_zip(response, filter_value, format):
    filter_value = "data" if not filter_value else filter_value

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zf:
        file_name = f"{filter_value}.{format}"
        data = zipfile.ZipInfo(file_name)
        data.date_time = time.localtime(time.time())[:6]
        data.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(data, response)

    memory_file.seek(0)

    return send_file(
        memory_file,
        attachment_filename=f"{filter_value}.zip",
        as_attachment=True
    )
