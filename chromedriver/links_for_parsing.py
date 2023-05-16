from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# url = "https://rus-ege.sdamgia.ru"

# user_agent = UserAgent()
# options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={user_agent.random}")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# options.add_argument('--disable-blink-features=AutomationControlled')
# driver = webdriver.Chrome(
# ChromeDriverManager().install(), options=options)
#     executable_path="/Users/alexeykashurnikov/PycharmProjects/exam_bot/chromedriver/chromedriver",
#     options=options
# )
# driver.get(url)
# html = driver.page_source


# with open('links_page.html', 'w') as file:
#     file.write(html)

links = []


with open('links_page.html') as file:
    src = file.read()


soup = BeautifulSoup(src, "lxml")
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


