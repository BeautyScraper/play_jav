import json
import random

def load_proxy_from_json(json_file_path):
    try:
        with open(json_file_path, 'r',encoding='utf-8') as json_file:
            proxy_data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    sel_p = random.choice(proxy_data)
    # breakpoint()
    proxy={
    "server": "165.227.44.211:3128"
    # "username": "usr",
    # "password": "pwd"
    }
    return  proxy