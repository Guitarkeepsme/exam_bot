from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
# import re
# import unicodedata

# занести в словарь номер задания, вопрос, текст и ответ

user_agent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent.random}")
driver = webdriver.Chrome(
    executable_path="/Users/alexeykashurnikov/PycharmProjects/exam_bot/chromedriver/chromedriver",
    options=options
)
all_tasks = []
url = "https://rus-ege.sdamgia.ru/test?theme=289"

try:
    xpath = "/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[4]"
    driver.get(url=url)
    time.sleep(3)
    wheel = driver.find_element(By.XPATH, xpath)
    wheel.click()

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
        all_tasks.append(task_id.get("id").replace("problem_", ""))
    print(all_tasks)
    number = 0
    for task in all_tasks:
        current_id = "sol" + str(task)
        r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
        soup = BeautifulSoup(r.text, "lxml")
        number += 1
        head = soup.find("div", class_="pbody").get_text()
        text = soup.find("div", class_="probtext").get_text()
        answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
        solution = soup.find("div", {"class": "solution"}, id=current_id).get_text()
        content = {
            "number": number,
            "head": head,
            "text": text,
            "answer": answer,
            "solution": solution
        }
        print(content)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

# r = requests.get(url)
# soup = BeautifulSoup(r.text, "lxml")
# for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
#     all_tasks.append(task_id.get("id").replace("problem_", ""))
# print(all_tasks)
# number = 0
# for task in all_tasks:
#     current_id = "sol" + str(task)
#     r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
#     soup = BeautifulSoup(r.text, "lxml")
#     number += 1
#     head = soup.find("div", class_="pbody").get_text()
#     text = soup.find("div", class_="probtext").get_text()
#     answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#     solution = soup.find("div", {"class": "solution"}, id=current_id).get_text()
#     content = {
#         "number": number,
#         "head": head,
#         "text": text,
#         "answer": answer,
#         "solution": solution
#     }
#     print(content)
