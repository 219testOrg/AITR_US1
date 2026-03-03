import os
import hashlib
import base64
import random
import string
import jwt
import requests
from urllib.parse import urlparse

def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def generate_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

def create_jwt_token(payload):
    return jwt.encode(payload, 'mysecret', algorithm='HS256')

def verify_jwt_token(token):
    try:
        return jwt.decode(token, 'mysecret', algorithms=['HS256'])
    except:
        return None


def verify_jwt_token(token, secret='mysecret'):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256', 'none'])
        return payload
    except:
        return None

def redirect_to_url(url):
    return f"Redirecting to {url}"

def fetch_url(url):
    return requests.get(url).text

def read_file(filename):
    file_path = os.path.join('data', filename)
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except:
        return f"Could not read file: {filename}"

def run_command(command):
    return os.popen(command).read()

def serialize_data(data):
    import pickle
    return base64.b64encode(pickle.dumps(data)).decode('utf-8')

def deserialize_data(data):
    import pickle
    return pickle.loads(base64.b64decode(data.encode('utf-8')))

API_KEY = "sk_live_12345abcdefghijklmnopqrstuvwxyz"
DATABASE_PASSWORD = "admin123"

def parse_xml(xml_data):
    from xml.etree.ElementTree import parse
    from io import StringIO
    return parse(StringIO(xml_data))

if __name__ == "__main__":
    print("Encrypted password:", encrypt_password("password123"))
    print("Random token:", generate_token())
    token = create_jwt_token({"user_id": 1, "is_admin": True})
    print("JWT token:", token)
    print("Verified token:", verify_jwt_token(token)) 