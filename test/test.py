import openai
from icecream import ic

# key = "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"
key = "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"
# key = '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'
# key = ""
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
user_input = input()
ic(user_input)
messages = update_chat(messages, "user", user_input)
ic(messages)
model_response = get_chatgpt_response(messages)
ic(model_response)
messages = update_chat(messages, "assistant", model_response)
ic(messages)
print_last_message(messages)
