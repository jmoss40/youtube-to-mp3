from flask import Flask, send_from_directory, jsonify, make_response
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from server import Server
import os, subprocess

HOST_NAME = "localhost"
PORT = 5000

app = Flask(__name__, static_url_path='', static_folder='../public')
CORS(app, expose_headers='content-disposition')
api = Api(app)

@app.route('/', defaults={'path':''})
def serve(path):
  return send_from_directory(app.static_folder, 'index.html')


@app.after_request
def response_processor(response):
    response.direct_passthrough = False
    file = response.headers['Content-Disposition']
    file = file[21:]
    
    os.chdir("/tmp")
    subprocess.call(['ls'])
    os.remove("./"+file)

    return response

api.add_resource(Server, '/download')

