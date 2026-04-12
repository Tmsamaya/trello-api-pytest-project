import json

from config import Config

def debug_response(response):
    print("\n--- RESPONSE START ---")
    print("(status:)", response.status_code)
    print("(text:)", response.text)
    print("--- RESPONSE END ---\n")

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return None

def print_object(data):
    print("\n--- RESPONSE START ---")
    print(json.dumps(data, indent=2, sort_keys=True))
    print("--- RESPONSE END ---\n")
    return

def debug_auth_inputs(key, token):
    formatted_key = format_auth_value(key, Config.TRELLO_KEY)
    formatted_token = format_auth_value(token, Config.TRELLO_TOKEN)

    print("\n--- Auth Input START ---")
    print("(key:)", formatted_key)
    print("(token:)", formatted_token)
    print("--- Auth Input END ---\n")

def format_auth_value(value, default_value):
    if value is None:
        return "<DEFAULT>" #Using real key/token from config
    if value == "":
        return "<EMPTY>"    #Intentially blank
    if value == default_value:
        return "<DEFAULT>"  #Fallback safety (in case we pass directly)

    return f"<Invalid:{value}>"