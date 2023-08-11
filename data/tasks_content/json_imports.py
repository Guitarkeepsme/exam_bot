import json
# import os


# working_directory = os.getcwd()
rus_path = '/Users/alexeykashurnikov/PycharmProjects/exam_bot/data/tasks_content/rus_content_310723.json'

with open(rus_path) as rus_data:
    rus_content = json.load(rus_data)


print(rus_path)
