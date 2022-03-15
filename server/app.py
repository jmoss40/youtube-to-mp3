import os
import subprocess
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from server import Server

HOST_NAME = "localhost"
PORT = 5000

app = Flask(__name__, static_url_path='', static_folder='../public')
CORS(app, expose_headers='content-disposition')
api = Api(app)


@app.route('/', defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


@app.after_request
def response_processor(response):
    response.direct_passthrough = False
    _file = response.headers['Content-Disposition']
    _file = _file[21:]

    os.chdir("/tmp")
    subprocess.call(['ls'])
    os.remove("./" + _file)

    return response


api.add_resource(Server, '/download')
