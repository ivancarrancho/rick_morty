import jwt
import hashlib


def encode_response(response, email=""):
    try:
        secret = hashlib.md5(email.encode('utf-8'))

        encoded_jwt = jwt.encode(
            response, secret.hexdigest(), algorithm="HS256"
        )

        return encoded_jwt
    except Exception as e:
        return f"Encode Error: {str(e)}"


def decode_response(response, email):
    try:
        secret = hashlib.md5(email.encode('utf-8'))

        return jwt.decode(response, secret.hexdigest(), algorithms=["HS256"])
    except Exception as e:
        return f"Decode Error: {str(e)}"
