from flask import Flask,redirect,url_for,request,jsonify, make_response, flash
from markupsafe import escape
from decouple import config
from flask_cors import CORS
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
import jsonpickle
from waitress import serve
import pathlib
from datetime import datetime
import requests
# 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
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
cors = CORS(app, resources={r"/prompt/": {"origins": config("ORIGIN")}})


@app.route('/prompt/',methods=['POST'])
def pom_extractor():
    token = request.headers.get('Authorization')
    print("TOKE IS: ", token)

    response= {"MSG": "OK"}
    return make_response(jsonify(response.json()))



if __name__ == "__main__":
    
    if config("MODE") == 'DEV':
        app.run(host='localhost', debug=True, port=5000)
    if config("MODE") == 'PROD':
        serve(app, host = '0.0.0.0', port=5000, threads = 4)