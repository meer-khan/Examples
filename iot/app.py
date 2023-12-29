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
import agg_pipelines, agg_pipeline_add
import authentication
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
allowed_origins = config("ORIGIN", default="").split(',')
ic(allowed_origins)
# Enable CORS for all routes that match the specified path
# cors = CORS(app, resources={r"/users/": {"origins": allowed_origins}})

cors = CORS(app, resources={r"/users/": {"origins": allowed_origins}, 
                             r"/addusers/": {"origins": allowed_origins},
                              r"/analytics/total_visits/": {"origins": allowed_origins},
                               r"/analytics/average_visits/": {"origins": allowed_origins},
                                r"/analytics/gender_trends/": {"origins": allowed_origins},
                                 r"/analytics/avg_gender_trends/": {"origins": allowed_origins}
                                 })


@app.route("/analytics/avg_gender_trends/", methods= ["GET"])
def avg_gender_trends():
    header = request.headers
    token = header.get("Authorization")
    if token != None: 
        result = authentication.verify_token(token)
        if result == False: 
            return make_response(jsonify({"error": "Authentication Failed"}), 401)
    else:
        return make_response(jsonify({"error": "Authentication Failed"}), 401)
     
    g_t_12m = agg_pipelines.monthly_visitors_count(cd)
    g_7h = agg_pipelines.gender_trend_last_7_hours(cd)

    g_t_12m.update(g_7h)


    result = json.dumps(g_t_12m)
    return make_response(result,200)

@app.route("/analytics/gender_trends/", methods= ["GET"])
def gender_trends(): 
    header = request.headers
    token = header.get("Authorization")
    if token != None: 
        result = authentication.verify_token(token)
        if result == False: 
            return make_response(jsonify({"error": "Authentication Failed"}), 401)
    else:
        return make_response(jsonify({"error": "Authentication Failed"}), 401)
    
    g_30d = agg_pipelines.gender_trend_30_days(cd)
    g_7w = agg_pipelines.gender_trend_last_7_weeks(cd)
    g_12m = agg_pipelines.gender_trend_12_months(cd)

    g_30d.update(g_7w)
    g_30d.update(g_12m)

    result = json.dumps(g_30d)
    return make_response(result,200)




@app.route("/analytics/average_visits/", methods= ["GET"])
def average_visits(): 
    header = request.headers
    token = header.get("Authorization")
    if token != None: 
        result = authentication.verify_token(token)
        if result == False: 
            return make_response(jsonify({"error": "Authentication Failed"}), 401)
    else:
        return make_response(jsonify({"error": "Authentication Failed"}), 401)
    
    # a_h = agg_pipelines.avg_hourly_visits(cd)
    # a_d = agg_pipelines.avg_daily_visit(cd)
    t_24h = agg_pipelines.hourly_visits_last_24h(cd)
    # ic(t_24h)
    t_7d = agg_pipelines.calculate_daily_visits_for_last_7d(cd)
    ic(t_7d)
    # result= agg_pipelines.avg_hourly_visits(cd)
    # print("********************")
    # print(result)
    busiest_hour = agg_pipelines.busiest_hour_7_days(cd)
    t_24h.update(t_7d)
    t_24h.update(busiest_hour)

    result = json.dumps(t_24h)
    return make_response(result,200)






@app.route("/analytics/total_visits/", methods= ["GET"])
def total_visits(): 
    try:
        header = request.headers
        token = header.get("Authorization")
        if token != None: 
            result = authentication.verify_token(token)
            if result == False: 
                return make_response(jsonify({"error": "Authentication Failed"}), 401)
        else:
            return make_response(jsonify({"error": "Authentication Failed"}), 401)
        # print(cursor:=cd.find())
        # for cur in cursor:
        #     print(cur)
        t_24h = agg_pipelines.total_visit_last_24_hours(cd)
        ic(t_24h)
        t_7d = agg_pipelines.total_visit_last_7_days(cd)
        ic(t_7d)
        c_t = agg_pipelines.total_male_female_kids_count_24h7d30d(cd)
        ic(c_t)
        
        t_24h.update(t_7d)
        t_24h.update(c_t)

        result = json.dumps(t_24h)
        return make_response(result,200)
    except Exception as ex: 
        return make_response(jsonify({"error":f"Exception: {ex}"}), 404)



@app.route("/daily_data/", methods= ["POST"])
def daily_data(): 
    try:
        data = request.json
        total_traffic = data.get("totalTraffic")
        total_male = data.get("totalMale")
        total_female = data.get("totalFemale")
        total_kids = data.get("totalKids")
        time_stamp = data.get("timeStamp")
        if total_traffic is None or total_male is None or total_female is None or total_kids is None: 
            result = {"error": "fields should not be none"}
            return make_response(jsonify(result), 400)
        dbquery.add_processed_data(cpd,total_traffic,total_male,total_female, total_kids,time_stamp)
        result = {"msg":"data added successfully"}
        return make_response(result,200)
    except Exception as ex: 
        return make_response(jsonify({"error":f"Exception: {ex}"}), 404)





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
        total_capacity = data.get("total_capacity")
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
                site_id = dbquery.add_site(cs, user_id, location, total_capacity)
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
    cu,cs,cd,cpd = db.main()
    if config("MODE") == 'DEV':
        app.run(host='0.0.0.0', debug=True, port=5000)
    if config("MODE") == 'PROD':
        serve(app, host = '0.0.0.0', port=5000, threads = 4)
        

# max_request_body_size = 2073741824