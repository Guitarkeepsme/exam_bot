from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


class TaskNumber:
    task_number = 4
    all_tasks = []


def parse_task(html):
    all_ids = []
    soup = BeautifulSoup(html, "lxml")
    for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
        all_ids.append(task_id.get("id").replace("problem_", ""))
        time.sleep(1)
    number = 0
    for id in all_ids:
        time.sleep(2)
        if soup.find("div", class_="probtext") is None:
            current_id = "sol" + str(id)
            r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(id))
            soup = BeautifulSoup(r.text, "lxml")
            number += 1
            head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
            if len(head) > 500:
                continue
            answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
            solution = soup.find("div", {"class": "solution"},
                                 id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
            content = {
                "number": number,
                "head": head,
                "answer": answer,
                "solution": solution
            }
            TaskNumber.all_tasks.append(content)
        else:
            current_id = "sol" + str(id)
            r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(id))
            soup = BeautifulSoup(r.text, "lxml")
            number += 1
            head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
            if len(head) > 500:
                continue
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
            TaskNumber.all_tasks.append(content)
    with open(f"russian_task{TaskNumber.task_number}.json", "w") as file:
        json.dump(TaskNumber.all_tasks, file, indent=4, ensure_ascii=False)


def get_source_html(url):
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    # options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.maximize_window()
    try:
        driver.get(url=url)
        time.sleep(3)
        while True:
            # find_more_element = driver.find_element(By.CLASS_NAME, "pager_page")

            parse_task(driver.page_source)

            # with open("test_2.html", "w") as file:
            #     file.write(driver.page_source)

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


# with open('test.html') as file:
#     src = file.read()


with open("tasks_links_2.json") as file:
    tasks_links = json.load(file)


def get_info(links):
    while TaskNumber.task_number <= 4:
        for task in links.get(str(TaskNumber.task_number)):
            url_base = "https://rus-ege.sdamgia.ru"
            get_source_html(url=url_base + task)
        TaskNumber.task_number += 1


def main():
    get_info(tasks_links)
    # get_source_html(url=url_all)


if __name__ == "__main__":
    main()

# dict_task_links = json.loads(tasks_links)
# print(dict_task_links)


