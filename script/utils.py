import json
#Saving and loading data
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
