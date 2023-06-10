from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time


class TaskNumber:
    task_number = 1


all_tasks = []

test_info = open('test_task.html', 'r')


def t_parse(html):
    current_id = "sol" + str(38775)
    soup_2 = BeautifulSoup(html, "lxml")
    example_number = 1
    # TaskNumber.example_number += 1
    head = soup_2.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
    if len(head) > 500:  # на случай если в заголовок попадёт теория по заданию
        return None
    answer = soup_2.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
    solution = soup_2.find("div", {"class": "solution"},
                         id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
    content = {
        "number": example_number,
        # "number": TaskNumber.example_number,
        "head": head,
        "answer": answer,  # нужно убрать слово "Ответ"
        "solution": solution  # нужно убрать слово "Пояснение"
    }
    all_tasks.append(content)


print(t_parse(test_info))
print(all_tasks)
