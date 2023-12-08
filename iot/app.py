from flask import Flask,redirect,url_for,request,jsonify, make_response, flash
from markupsafe import escape
from decouple import config
from flask_cors import CORS
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os, json
import jsonpickle
from waitress import serve
import pathlib
from datetime import datetime
import requests
import openai
from icecream import ic
import db, dbquery
from bson import json_util

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
cors = CORS(app, resources={r"/users/": {"origins": config("ORIGIN")}})







@app.route('/users/',methods=['GET'])
def get_users():
    if request.method == "GET":
        try:
            cu,cs,cd = db.main()
            users = dbquery.get_users(cu)
            ic(users)
            # result = json.dumps(users, default= json_util.default)
            result = json.dumps(users)
            return make_response(result, 200)
        except Exception as e:
            # Handle other exceptions
            error_message = f"An unexpected error occurred: {str(e)}"
            return make_response(jsonify({'error': error_message}), 500)
    
    if request.method == "POST":
        try: 
            pass
        except:
            pass




if __name__ == "__main__":
        
    if config("MODE") == 'DEV':
        app.run(host='localhost', debug=True, port=5000)
    if config("MODE") == 'PROD':
        serve(app, host = '0.0.0.0', port=5000, threads = 4)
        

# max_request_body_size = 2073741824