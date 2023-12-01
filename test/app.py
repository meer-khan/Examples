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
# 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
# organizationID: org-vO1XmiqVug26vPS20hBFcnrE
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
cors = CORS(app, resources={r"/prompt/": {"origins": config("ORIGIN")}})

key = "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"
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

# Your existing code
messages = [
    {"role": "user", "content": "   "},
    {"role": "assistant", "content": "   "},
]

# while True:
print_last_message(messages)
user_input = input()
messages = update_chat(messages, "user", user_input)
model_response = get_chatgpt_response(messages)
messages = update_chat(messages, "assistant", model_response)




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