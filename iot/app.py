from flask import Flask,redirect,url_for,request,jsonify, make_response, flash
from markupsafe import escape
from decouple import config
from flask_cors import CORS
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os, json, hashlib
import jsonpickle
from waitress import serve
from icecream import ic
import db, dbquery
from bson import json_util

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
cors = CORS(app, resources={r"/users/": {"origins": config("ORIGIN")}})




@app.route('/addusers/',methods=["POST"])
def add_user():
    try:
        data = request.json
        brand_name = data.get("brandName")
        email = data.get("email")
        # password = hashlib.sha256(data.get("password").encode()).hexdigest()
        password = data.get("password")

        location = data.get("location")
        if brand_name is None or email is None or password is None or location is None: 
            result = {"error": "No field should be none"}
            return make_response(jsonify(result), 400)
        
        result = dbquery.add_user(cu,brand_name,email,password,location)
        return make_response(jsonify({"msg":f"User added successfully with id {result}"}), 201)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return make_response(jsonify({'error': error_message}), 500)



@app.route('/users/',methods=['GET', "POST"])
def user():
    
    if request.method == "GET":
        try:
            
            users = dbquery.get_users(cu)
            # ic(users)
            # result = json.dumps(users, default= json_util.default)
            result = json.dumps(users)
            return make_response(result, 200)
        except Exception as e:
            # Handle other exceptions
            error_message = f"An unexpected error occurred: {str(e)}"
            return make_response(jsonify({'error': error_message}), 500)
    
    if request.method == "POST":
        data = request.json
        user_id = data.get("userID")
        location = data.get("location")
        no_of_people = data.get("noOfPeople")
        total_traffic = data.get("totalTraffic")
        total_male = data.get("totalMale")
        total_female = data.get("totalFemale")
        total_kids = data.get("totalKids")

        if user_id is None or location is None or no_of_people is None or total_traffic is None or total_male is None or total_female is None or total_kids is None: 
            result = {"error": "fields should not be none"}
            return make_response(jsonify(result), 400)



        try: 
            user = dbquery.get_one_user(cu,user_id)
            if user:
                site_id = dbquery.add_site(cs, user_id, location)
                dbquery.add_data(cd,site_id,user_id,no_of_people,total_traffic,total_male,total_female, total_kids)
                result = {"msg":"data added successfully"}
                return make_response(jsonify(result), 201)
            else: 
                result = {"error": "User not found"}
                return make_response(jsonify(result), 400)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return make_response(jsonify({'error': error_message}), 500)





if __name__ == "__main__":
    cu,cs,cd = db.main()
    if config("MODE") == 'DEV':
        app.run(host='localhost', debug=True, port=5000)
    if config("MODE") == 'PROD':
        serve(app, host = '0.0.0.0', port=5000, threads = 4)
        

# max_request_body_size = 2073741824