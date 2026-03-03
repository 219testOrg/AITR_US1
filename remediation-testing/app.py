from flask import Flask, request, render_template_string
import os
import subprocess
import yaml
import pickle
import sqlite3

app = Flask(__name__)

user_data = {
    '1': {'username': 'admin', 'balance': 1000},
    '2': {'username': 'user', 'balance': 500}
}


def get_user_from_db(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    c.execute(query)
    return c.fetchone()


@app.route('/')
def index():
    return "Welcome to the Vulnerable Python App"


@app.route('/ping')
def ping():
    ip = request.args.get('ip', '8.8.8.8')
    cmd = "ping -c 1 " + ip
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


@app.route('/load_settings')
def load_settings():
    data = request.args.get('data', '')
    if data:
        settings = pickle.loads(data.encode('latin1'))
        return str(settings)
    return "No settings provided"


@app.route('/parse_yaml')
def parse_yaml():
    yaml_data = request.args.get('data', '')
    if yaml_data:
        parsed_data = yaml.load(yaml_data)
        return str(parsed_data)
    return "No YAML data provided"


@app.route('/page')
def page():
    name = request.args.get('name', '')
    template = '<h1>Hello, ' + name + '!</h1>'
    return render_template_string(template)


@app.route('/file')
def get_file():
    filename = request.args.get('filename', '')
    with open(os.path.join('files', filename), 'r') as f:
        content = f.read()
    return content


if __name__ == "__main__":
    app.run(debug=True) 