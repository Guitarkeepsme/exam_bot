import json
import os


working_directory = os.getcwd()
rus_path = working_directory + '/data/tasks_content/russian_content.json'

with open(rus_path) as rus_data:
    rus_content = json.load(rus_data)


