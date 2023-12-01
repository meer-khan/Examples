from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
# openai.api_key = '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'
openai.api_key = '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'
messages = [
        {"role": "user", "content": "   "},
        {"role": "assistant", "content": "   "},
    ]
def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages
    )
    return response['choices'][0]['message']['content']

def print_last_message(messages):
    if messages:
        last_message = messages[-1]
        print(last_message["role"] + ": " + last_message["content"])

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data['question']

        messages = update_chat(messages, "user", user_input)
        model_response = get_chatgpt_response(messages)
        messages = update_chat(messages, "assistant", model_response)

        return jsonify({'assistant_response': model_response})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':

    app.run(debug=True)
