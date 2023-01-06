from bs4 import BeautifulSoup
import requests
# import re
# import unicodedata

# занести в словарь номер задания, вопрос, текст и ответ


all_tasks = []
url = "https://rus-ege.sdamgia.ru/test?theme=289"
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
    head = soup.find("div", {"class": "pbody"}).get_text()
    text = soup.find("div", {"class": "probtext"}).get_text()
    answer = soup.find("div", {"class": "solution"}, id=current_id).get_text()
    content = {
        "number": number,
        "head": head,
        "text": text,
        "answer": answer
    }

    print(content)
