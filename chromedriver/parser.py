from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


url_base = "https://rus-ege.sdamgia.ru"
url_end = "/test?theme=341"
url_all = url_base + url_end


def get_source_html(url):
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    # options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.maximize_window()
    # html = driver.page_source
    try:
        driver.get(url=url)
        time.sleep(3)
        while True:
            # find_more_element = driver.find_element(By.CLASS_NAME, "pager_page")

            with open("test_2.html", "w") as file:
                file.write(driver.page_source)

            if "Пройти тестирование" in driver.find_elements(By.LINK_TEXT, "a"):
                break
            else:
                scroll_value = 1000
                scroll_by = f'window.scrollBy(0, {scroll_value});'
                driver.execute_script(scroll_by)
                time.sleep(1)
                # counter += 1

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def parse_task(html):
    all_tasks = []
    soup = BeautifulSoup(html, "lxml")
    for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
        all_tasks.append(task_id.get("id").replace("problem_", ""))
    number = 0
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
                "answer": answer,
                "solution": solution
            }
        else:
            if "Чаще всего в" in soup.find_all("div", class_="pbody"):
                break
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
                "text": text,
                "answer": answer,
                "solution": solution
            }

        print(content)
    pass


with open('test.html') as file:
    src = file.read()


def main():
    # get_source_html(url=url_all)
    parse_task(src)


if __name__ == "__main__":
    main()





# for page in selenium_pages:
#     soup = BeautifulSoup(page, "lxml")
#     for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
#         all_tasks.append(task_id.get("id").replace("problem_", ""))
#
#
# for task in all_tasks:
#     if soup.find("div", class_="probtext") is None:
#         current_id = "sol" + str(task)
#         r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
#         soup = BeautifulSoup(r.text, "lxml")
#         number += 1
#         head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#         solution = soup.find("div", {"class": "solution"},
#                              id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#         content = {
#             "number": number,
#             "head": head,
#             # "text": text,
#             "answer": answer,
#             "solution": solution
#         }
#     else:
#         current_id = "sol" + str(task)
#         r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(task))
#         soup = BeautifulSoup(r.text, "lxml")
#         number += 1
#         head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         text = soup.find("div", class_="probtext").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#         solution = soup.find("div", {"class": "solution"},
#                              id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#         content = {
#             "number": number,
#             "head": head,
#             "text": text,
#             "answer": answer,
#             "solution": solution
#         }
#
#     print(content)
#
# print(all_tasks)
