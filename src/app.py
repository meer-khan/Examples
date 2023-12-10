from flask import Flask,redirect,url_for,request,jsonify, make_response, flash
from decouple import config
from flask_cors import CORS
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from waitress import serve
import openai
from icecream import ic
import pandas as pd
from werkzeug.utils import secure_filename
import pathlib
import uuid, os

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = config("uploadFolder")
cors = CORS(app, resources={r"/prompt/": {"origins": config("ORIGIN")}})
app.config['UPLOAD_FOLDER'] = config("uploadFolder")
ALLOWED_EXTENSIONS = (".xlsx", )
# Get a list of values
# allowed_hosts = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

key = config("KEY")
openai.api_key = key

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


def get_chatgpt_response(messages, tokens):
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages, 
        max_tokens = tokens
    )
    # ic(response)
    return response['choices'][0]['message']['content']


def get_file_content(file_path):
    # file_path = r'D:\2022\Examples\test\Test 2.xlsx'

    df = pd.read_excel(file_path)
    sample_data = df.head(20).to_string(index=False)
    return sample_data

def initiate_context():
    context = [{"role":"system", "content": "consider yourself as strategist and implementor"}]
    return context

def get_extension(file):
    return pathlib.Path(file).suffix

def generate_unique_name(file_name):
    return file_name+ str(uuid.uuid4())

def validate_data(shop_categories,content_concept_n_narrative,seasionality,key_e_commerce_dates,industry_specific_key_days,shop_locations):
    
    if shop_categories == None: 
            shop_categories = "online store"

    if content_concept_n_narrative == None: 
        content_concept_n_narrative = "relevant to shop categories for US market"

    if seasionality == None: 
        seasionality = "current season"

    if key_e_commerce_dates == None: 
        key_e_commerce_dates = "1 month"

    if industry_specific_key_days == None: 
        industry_specific_key_days = "relevant to shop categories"

    if shop_locations == None: 
        shop_locations = "online store"
    

    return shop_categories, content_concept_n_narrative, seasionality, key_e_commerce_dates, industry_specific_key_days, shop_locations




@app.route('/prompt/',methods=['POST'])
def pom_extractor():
    # try:
        messages = initiate_context()
        print(messages)
        # data = request.get_json()


        # ques = request.form.get('question')
        # Get the file from the form data
        file = request.files.get('file') 


        shop_categories = request.form.get('shop_categories')
        content_concept_n_narrative = request.form.get('ccn')
        seasionality = request.form.get('seasionality')
        key_e_commerce_dates = request.form.get('ked')
        industry_specific_key_days = request.form.get('iskd')
        shop_locations = request.form.get('shop_locations')
        
        shop_categories, content_concept_n_narrative, seasionality, key_e_commerce_dates, industry_specific_key_days, shop_locations= validate_data(shop_categories, 
                                                                                                                                                    content_concept_n_narrative, 
                                                                                                                                                    seasionality,
                                                                                                                                                    key_e_commerce_dates, 
                                                                                                                                                    industry_specific_key_days, 
                                                                                                                                                    shop_locations)
        prompt = f'''
            "Please Rephrase this given text in 60 words, "Generate weekly calendar campaigns, for the shopify store
                            {shop_categories} with a focus on {content_concept_n_narrative}
                            around {seasionality}, considering for {key_e_commerce_dates} and {industry_specific_key_days},
                            targeted at {shop_locations},  
                            I want you to return a table with campaign ideas, reasoning, targeted audiences."  
            '''
        
        result = update_chat(messages, role="user", content=prompt)
        ic("1st CALL OF CHATGPT")
        rephrased_text = get_chatgpt_response(result, 70)
        result = update_chat(result, role="assistant", content=rephrased_text)

        if request.files.get("file") is None: 
            ques = f'''
                Please Generate weekly calendar campaigns, next 3 months from now, for the shopify store
                {shop_categories} with a focus on {content_concept_n_narrative}
                around {seasionality}, considering {key_e_commerce_dates} and {industry_specific_key_days},
                targeted at {shop_locations}, 
                consider yourself as strategist and implementor and also emphasize to generate data in tabular. 
                I want you to return a table with campaign ideas, reasoning, targeted audiences, Prompt should be 
                tailored according to seasonality, trends, shop category, what the shops products are, key e-commerce days, 
                3 days a week at least. 
            '''
            result = update_chat(messages=result, role='user', content=ques)
            ic("2nd CALL OF CHATGPT")
            response = get_chatgpt_response(result, 4096)
            print(response)

            # NEW CODE
            result = update_chat(messages=result, role='assistant', content=response)
            prompt = 'Generate HTML code of above table'
            result = update_chat(messages=result, role='user', content=prompt)

            response = get_chatgpt_response(result, 4096)

            print(response)


            # END CODE



            final_output = {"rephrasedPrompt":rephrased_text, "response": response}
            return make_response(jsonify(final_output), 200)

        elif request.files.get("file") is not None:
            ic("FILE RECEIVED")
            file_name = secure_filename(file.filename)
            ext = get_extension(file_name)
            if ext  not in ALLOWED_EXTENSIONS:
                return make_response(jsonify({"error": "Invalid Input File, It Should Be in .xlsx Format"}), 400)
            Uname = generate_unique_name(file_name)
            file_path  = os.path.join(config('uploadFolder'), Uname)
            file.save(file_path)
            data = get_file_content(file_path)

            result = update_chat(messages=result, role="user", content=data)
            ic("2nd CALL OF CHATGPT")
            response = get_chatgpt_response(result, 4096)
            result = update_chat(messages=result, role='assistant', content=response)
            final_prompt = f"Please suggest atleast 1 product for each weekly calendar campaigns for {key_e_commerce_dates} in tabular form. Use above data to generate campaign."
            result = update_chat(messages=result, role='user', content=final_prompt)
            ic("3rd CALL OF CHATGPT")
            response = get_chatgpt_response(result, 4096)
            result = update_chat(messages=result, role='assistant', content=response)
            final_prompt = "Convert this table into HTML Tables"
            result = update_chat(messages=result, role='user', content=final_prompt)
            response = get_chatgpt_response(result, 4096)
            print(response)
            final_output = {"rephrasedPrompt":rephrased_text, "response": response}
            os.remove(file_path)
            return make_response(jsonify(final_output), 200)
        else: 
            error_message = {"error":{"Data is Incomplete"}}
            return make_response(jsonify(error_message), 400)
    # except Exception as e:
    #     # Handle other exceptions
    #     error_message = f"An unexpected error occurred: {str(e)}"
    #     return make_response(jsonify({'error': error_message}), 500)



if __name__ == "__main__":
    os.makedirs(config("uploadFolder"),exist_ok=True)
    if config("MODE") == 'DEV':
        app.run(host='localhost', debug=True, port=5000)
    if config("MODE") == 'PROD':
        serve(app, host = '0.0.0.0', port=5000, threads = 4)
        

# max_request_body_size = 2073741824