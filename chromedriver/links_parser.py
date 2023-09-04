import json

from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

url = "https://mathb-ege.sdamgia.ru/prob-catalog"

user_agent = UserAgent()
service = Service()
options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={user_agent.random}")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install(), service=service, options=options)
driver.get(url)
html = driver.page_source


# with open('links_page.html', 'w') as file:
#     file.write(html)

soup = BeautifulSoup(html, "html")
print(soup)
# with open('links_page.html') as file:
#     src = file.read()
# soup = BeautifulSoup(src, "lxml")

all_titles = {}
number = 0
for task in (soup.find_all("div", {"class": "ConstructorForm-Topic"})):
    title = []
    links = []
    task_title = task.find("u", {"class": "Link-U Link_wrap-U Link_pseudo-U Link_pseudoBlack-U"})
    task_links = task.find_all("a", {"class": "Link Link_black"})
    if task_title:
        title.append(task_title.text.replace("\xad", ""))
        number += 1
    for task_link in task_links:
        links.append(task_link.get("href"))
    if "Задания, не" in task.text:
        break
    if task_title:
        all_titles.update({number: tuple(links)})

        with open("tasks_links_3.json", "w") as file:
            json.dump(all_titles, file, indent=4, ensure_ascii=False)
print(all_titles)
# print(tasks_titles)
# print(len(tasks_titles))






