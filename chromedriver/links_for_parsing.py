from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
# from selenium.webdriver.common.by import By

url = "https://rus-ege.sdamgia.ru"

user_agent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(
    executable_path="/Users/alexeykashurnikov/PycharmProjects/exam_bot/chromedriver/chromedriver",
    options=options
)
links = []
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

for task in soup.find_all("div", {"class": "ConstructorForm-TopicDesc"}):
    print(task)
    result = task.get('href')
    print(result)


# for link in soup.find_all("a", {"class": "Link Link_black"}):
#     # if ограничить фразой "Задания, не входящие в ЕГЭ этого года":
#     # break
#     result = link.get('href')
#     print(result)
#     links.append(result)
#     counter += 1

print(links)


