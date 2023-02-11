from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
# import re
# import unicodedata

# занести в словарь номер задания, вопрос, текст и ответ
content = {}
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
all_tasks = []
selenium_pages = []
url = "https://rus-ege.sdamgia.ru/test?theme=205"
number = 0
task_counter = 0

xpath_1 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[1]"
driver.get(url=url)
time.sleep(1)
wheel = driver.find_element(By.XPATH, xpath_1)
wheel.click()
page_source = driver.page_source
selenium_pages.append(page_source)



# xpath_2 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[2]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_2)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_3 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[3]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_3)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_4 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[4]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_4)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_5 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[5]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_5)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_6 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[6]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_6)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_7 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[7]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_7)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_8 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[8]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_8)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_9 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[9]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_9)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)
#
# xpath_10 = f"/html/body/div[1]/div[5]/div[1]/div[4]/div[1]/span[10]"
# driver.get(url=url)
# time.sleep(1)
# wheel = driver.find_element(By.XPATH, xpath_10)
# wheel.click()
# page_source = driver.page_source
# selenium_pages.append(page_source)

driver.close()
driver.quit()

for page in selenium_pages:
    soup = BeautifulSoup(page, "lxml")
    for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
        all_tasks.append(task_id.get("id").replace("problem_", ""))


for task in all_tasks:
    if soup.find("div", class_="probtext") is None:
        current_id = "sol" + str(task)
        r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
        soup = BeautifulSoup(r.text, "lxml")
        number += 1
        head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
        answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
        solution = soup.find("div", {"class": "solution"},
                             id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
        content = {
            "number": number,
            "head": head,
            # "text": text,
            "answer": answer,
            "solution": solution
        }
    else:
        current_id = "sol" + str(task)
        r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
        soup = BeautifulSoup(r.text, "lxml")
        number += 1
        head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
        text = soup.find("div", class_="probtext").get_text().replace("\u202f", " ").replace("\xa0", " ")
        answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
        solution = soup.find("div", {"class": "solution"},
                             id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
        content = {
            "number": number,
            "head": head,
            # "text": text,
            "answer": answer,
            "solution": solution
        }

    print(content)

print(all_tasks)
