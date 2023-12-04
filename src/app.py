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
import openai
from icecream import ic

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
cors = CORS(app, resources={r"/prompt/": {"origins": config("ORIGIN")}})


# .env 
# ALLOWED_HOSTS=localhost,127.0.0.1
# Get a list of values
# allowed_hosts = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

# key = config("KEY")
# openai.api_key = key


# response = openai.ChatCompletion.create(
#   model="gpt-4-1106-preview",
#   messages=[
#         {"role": "user", "content": ""},
#     ]
# )

# def update_chat(messages, role, content):
#     messages.append({"role": role, "content": content})
#     return messages


# def get_chatgpt_response(messages):
#   response = openai.ChatCompletion.create(
#   model="gpt-4-1106-preview",
#   messages=messages
# )
#   return  response['choices'][0]['message']['content']


# def print_last_message(messages):
#     if messages:
#         last_message = messages[-1]
#         print(last_message["role"] + ": " + last_message["content"])

# def get_last_message(messages):
#     if messages:
#         last_message = messages[-1]
#         return last_message["role"] + ": " + last_message["content"]

'''
You are an email marketer for online [sneaker e-commerce store] , 
can you suggest a list of email campaigns by looking at trends ,
[holidays , sports and entertainment events , calendars] , what’s hot 
topic on [social media]  in the recent [months] , hot topics in relevant industries and 
consumer behaviors etc ? Please be creative and be relevant , targeting [young professionals , 
university students , urban and rural populations]

Generate an email campaign calendar for [sports] with a focus on [stay healthy 
and physically healthy] around [summer], considering [summer holidays] and, targeted at [F10, 
Islamabad Pakistan]
'''
# f'''
# You are an email marketer for online {shop_categories} , 
# can you suggest a list of email campaigns by looking at trends ,
# {content_concept_n_narrative} , what’s hot 
# topic on social media  in the recent {seasionality} , hot topics in relevant industries and 
# consumer behaviors etc ? Please be creative and be relevant , targeting {shop_locations}

# '''


# PREVIOUS PARAMS
'''

{
    "shop_categories": "sports", 
    "ccn": "stay healthy and physically healthy",  //Content concept and narrative
    "seasionality": "winter", 
    //"ked": "winter holidays", //Key E-commerce Dates
    //"iskd": "", //Industry-Specific Key Days
    "shop_locations": "4802 Rockwell Lane,  Rocky Mount, North Carolina"
}

'''






@app.route('/prompt/',methods=['POST'])
def pom_extractor():
    try:
        messages = [
        {"role": "user", "content": "   "},
        {"role": "assistant", "content": "   "},
        ]

        '''Generate an email campaign calendar for [Shop Categories] 
        with a focus on [Content concept and narrative] 
        around [seasonality], 
        considering [Key E-commerce Dates] and [Industry-Specific Key Days], targeted at [Shop Locations].'''
        data = request.get_json()
        # ques = data.get("question","")

        shop_categories = data.get("shop_categories", " ")
        content_concept_n_narrative = data.get("ccn", " ")
        seasionality = data.get("seasonality", " ")
        key_e_commerce_dates = data.get("ked", " ")
        industry_specific_key_days = data.get("iskd", " ")
        shop_locations = data.get("shop_locations"," ")

        # * OUR STRING FOR PROMPT ENGINEERING
        # ques = f'''Generate an email campaign calendar for {shop_categories} 
        # with a focus on {content_concept_n_narrative} 
        # around {seasionality}, 
        # considering {key_e_commerce_dates} and {industry_specific_key_days}, targeted at {shop_locations}.'''


        # *: NEW CODE
        ques = f'''
                Please create and rephrase Prompt for weekly calendar campaigns, next 3 months from now, for the shopify store
                {shop_categories} with a focus on {content_concept_n_narrative}
                around {seasionality}, considering {key_e_commerce_dates} and {industry_specific_key_days},
                targeted at {shop_locations}, 
                consider yourself as strategist and implementor and also emphasize to generate data in tabular. 
                I want you to return a table with campaign ideas, reasoning, targeted audiences, Prompt should be 
                tailored according to seasonality, trends, shop category, what the shops products are, key e-commerce days, 
                3 days a week at least. 
            '''
# Please act like a strategist and implementor and generate relevant chatgpt prompt to get above results.
# Please generate relevant chatgpt prompt to get above results.
        # ques = '''
        #     Please create and rephrase only Prompt for weekly calendar campaigns, next 3 months from now, for the 
        #     shopify “sports and lifestyle clothing  with a focus Stay physically healtyh and active, around winter at  
        #     4802 Rockwell Lane,  Rocky Mount, North Carolina”, consider yourself as strategist and implementor and also 
        #     emphasize to generate data in tabular. I want you to return a table with campaign ideas, reasoning, 
        #     targeted audiences, Prompt should be tailored according to seasonality, trends, shop category, what the shops products
        #     are, key e-commerce days, 3 days a week at least.

        #     '''

        # ques = '''
        #     Please create and rephrase only Prompt for weekly calendar campaigns, 
        #     next 3 months from now, for the shopify sports and lifestyle clothing  with a focus Stay physically 
        #     healtyh and active, around winter at  4802 Rockwell Lane,  Rocky Mount, North Carolina, 

        #     consider yourself as strategist and implementor, Prompt should be tailored according to seasonality, 
        #     trends, shop category, what the shops products are, key e-commerce days,
        #     '''

        # *: END CODE




        messages = update_chat(messages, "user", ques)
        # ic(messages)
        model_response = get_chatgpt_response(messages)
        # ic(model_response)
        messages = update_chat(messages, "assistant", model_response)
        # ic(messages)
        print_last_message(messages)
        result = get_last_message(messages)
        result = {"response": result}
        return make_response(jsonify(result), 200)
    except Exception as e:
        # Handle other exceptions
        error_message = f"An unexpected error occurred: {str(e)}"
        return make_response(jsonify({'error': error_message}), 500)



if __name__ == "__main__":

    key = config("KEY")
    openai.api_key = key
    response = openai.ChatCompletion.create(
    model="gpt-4-1106-preview",
    messages=[
            {"role": "user", "content": ""},
        ]
    )

    def update_chat(messages, role, content):
        messages.append({"role": role, "content": content})
        return messages


    def get_chatgpt_response(messages):
        response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
        )
        return  response['choices'][0]['message']['content']


    def print_last_message(messages):
        if messages:
            last_message = messages[-1]
            print(last_message["role"] + ": " + last_message["content"])

    def get_last_message(messages):
        if messages:
            last_message = messages[-1]
            return last_message["role"] + ": " + last_message["content"]
        
    if config("MODE") == 'DEV':
        app.run(host='localhost', debug=True, port=5000)
    if config("MODE") == 'PROD':
        serve(app, host = '0.0.0.0', port=5000, threads = 4)
        

# max_request_body_size = 2073741824