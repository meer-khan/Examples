import uuid

tokens = ("ea5ce7ef-82e7-480d-9acd-b0fefb5b810d",)

def get_token():
    return str(uuid.uuid4())

def verify_token(token):
    return True if token in tokens else False


if __name__ == "__main__":
    t = get_token()
    print(t)

