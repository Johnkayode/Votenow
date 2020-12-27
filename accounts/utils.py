import random
import base64


def generate_code():
    return random.randrange(100000, 999999)

def encode_data(data):
    data_bytes = data.encode('ascii')
    data = base64.b64encode(data_bytes)
    data = data.decode('ascii')
    return data

def decode_data(data):
    data_bytes = data.encode('ascii')
    data = base64.b64decode(data_bytes)
    data = data.decode('ascii')
    return data