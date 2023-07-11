import base64
from werkzeug import datastructures


def encode_image(image: datastructures.FileStorage):
    return base64.b64encode(image.read())


def decode_image(image: bytes):
    return image.decode()
