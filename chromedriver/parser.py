from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


# ПОСЛЕ ДОЛГИХ МЫТАРСТВ РЕШИЛ СДЕЛАТЬ ПАРСИНГ ТАКИМ:
# Сначала проходим по странице и парсим айдишники заданий, избегая повторов
# Затем проходим ещё раз, парсим уже сами задания
# Здесь вырисовывается две проблемы: во-первых, два прохода делать не хотелось бы, а во-вторых,
# пока не понятно, как я буду очищать список, если прошёл все задания
# может быть, сначала загрузить в файл айдишники, а потом уже парсить информацию?


class TaskNumber:
    task_number = 1
    # example_number = 0    # счётчик номеров конкретного задания
    all_ids = []
    all_tasks = []  # здесь будет храниться вся полученная инфа. Создал класс, чтобы работать с ней внутри всех функций
    # all_tasks_set = set(all_tasks)


ids = {}
result_links = []  # сохраняем ссылки, вернее айдишники, в списке


def parse_id(html):
    soup = BeautifulSoup(html, "lxml")
    for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
        result = task_id.get("id").replace("problem_", "")
        if result not in result_links:
            result_links.append(result)


# def parse_task(html):
#     soup = BeautifulSoup(html, "lxml")
#     example_number = 0    # счётчик номеров конкретного задания
#     for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
#         result = task_id.get("id").replace("problem_", "")
#         if result not in ids:
#             ids.append(result)
#     for t_id in ids:
#         print(t_id)
#         # if soup.find("div", class_="probtext") is None:
#         current_id = "sol" + str(t_id)
#         r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(current_id))
#         soup_2 = BeautifulSoup(r.text, "lxml")
#         print(soup_2)
#         example_number += 1
#         # TaskNumber.example_number += 1
#         head = soup_2.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         if len(head) > 500:  # на случай если в заголовок попадёт теория по заданию
#             continue
#         answer = soup_2.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#         solution = soup_2.find("div", {"class": "solution"},
#                              id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#         content = {
#             "number": example_number,
#             # "number": TaskNumber.example_number,
#             "head": head,
#             "answer": answer,  # нужно убрать слово "Ответ"
#             "solution": solution  # нужно убрать слово "Пояснение"
#         }
#         TaskNumber.all_tasks.append(content)
#         # else:
#         # current_id = "sol" + str(t_id)
#         # r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(current_id))
#         # soup_2 = BeautifulSoup(r.text, "lxml")
#         # example_number += 1
#         # # TaskNumber.example_number += 1
#         # head = soup_2.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         # if len(head) > 500:
#         #     continue
#         # text = soup_2.find("div", class_="probtext").get_text().replace("\u202f", " ").replace("\xa0", " ")
#         # answer = soup_2.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#         # solution = soup_2.find("div", {"class": "solution"},
#         #                      id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#         # content = {
#         #     "number": example_number,
#         #     # "number": TaskNumber.example_number,
#         #     "head": head,
#         #     "text": text,
#         #     "answer": answer,  # нужно убрать слово "Ответ"
#         #     "solution": solution  # нужно убрать слово "Пояснение"
#         # }
#         # TaskNumber.all_tasks.append(content)
#         with open(f"russian_task{TaskNumber.task_number}.json", "a") as file:
#             json.dump(TaskNumber.all_tasks, file, indent=4,
#                       ensure_ascii=False)  # закидываем всё в отдельный файл


# def parse_task(html):
#     all_ids = []  # для удобства создал отдельный список айдишников
#     soup = BeautifulSoup(html, "lxml")
#     example_number = 0    # счётчик номеров конкретного задания
#     # for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
#     #     result = task_id.get("id").replace("problem_", "")
#     #     if result not in TaskNumber.all_tasks:
#     #         TaskNumber.all_ids.append(result)
#     #     elif len(TaskNumber.all_tasks) > 10:
#     #         break
#     for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
#         result = task_id.get("id").replace("problem_", "")
#         if result not in test_all:
#             test_all.append(result)
#     #     elif len(test_all) > 10:
#     #         break
#     for t_id in TaskNumber.all_ids:
#         # time.sleep(1)
#         if soup.find("div", class_="probtext") is None:
#             current_id = "sol" + str(t_id)
#             r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(t_id))
#             soup = BeautifulSoup(r.text, "lxml")
#             example_number += 1
#             # TaskNumber.example_number += 1
#             head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#             if len(head) > 500:  # на случай если в заголовок попадёт теория по заданию
#                 continue
#             answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#             solution = soup.find("div", {"class": "solution"},
#                                  id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#             content = {
#                 "number": example_number,
#                 # "number": TaskNumber.example_number,
#                 "head": head,
#                 "answer": answer,  # нужно убрать слово "Ответ"
#                 "solution": solution  # нужно убрать слово "Пояснение"
#             }
#             TaskNumber.all_tasks.append(content)
#         else:
#             current_id = "sol" + str(t_id)
#             r = requests.get("https://rus-ege.sdamgia.ru/problem?id=" + str(t_id))
#             soup = BeautifulSoup(r.text, "lxml")
#             example_number += 1
#             # TaskNumber.example_number += 1
#             head = soup.find("div", class_="pbody").get_text().replace("\u202f", " ").replace("\xa0", " ")
#             if len(head) > 500:
#                 continue
#             text = soup.find("div", class_="probtext").get_text().replace("\u202f", " ").replace("\xa0", " ")
#             answer = soup.find("div", class_="solution", id=current_id).find_next_sibling().get_text()
#             solution = soup.find("div", {"class": "solution"},
#                                  id=current_id).get_text().replace("\u202f", " ").replace("\xa0", " ")
#             content = {
#                 "number": example_number,
#                 # "number": TaskNumber.example_number,
#                 "head": head,
#                 "text": text,
#                 "answer": answer,  # нужно убрать слово "Ответ"
#                 "solution": solution  # нужно убрать слово "Пояснение"
#             }
#             TaskNumber.all_tasks.append(content)
#             with open(f"russian_task{TaskNumber.task_number}.json", "a") as file:
#                 json.dump(TaskNumber.all_tasks, file, indent=4,
#                           ensure_ascii=False)  # закидываем всё в отдельный файл


def get_source_html(url):
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent.random}")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get(url=url)
        time.sleep(2)
        reached_page_end = False  # для того, чтоб дойти до конца страницы, создаём переменную
        last_height = driver.execute_script("return document.body.scrollHeight")  # запоминаем высоту
        print(last_height)
        while not reached_page_end:
            time.sleep(2)
            parse_id(driver.page_source)
            scroll_value = 1500
            scroll_by = f'window.scrollBy(0, {scroll_value});'
            driver.execute_script(scroll_by)
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")  # берём новые данные о высоте
            print(new_height)
            if last_height == new_height or last_height > 10000:  # проверяем, переместились ли мы вниз, и если нет, то
                reached_page_end = True    # заканчиваем
            else:                          # иначе меняем показатель высоты и продолжаем
                last_height = new_height
            print(result_links)
            # if int(soup.find("div", class_="prob_num").get_text()) == len(TaskNumber.all_tasks):
            # actions = ActionChains(driver)
            # print(test_all)
            # print(TaskNumber.all_ids)
            # parse_task(driver.page_source)
            # element = driver.find_element(By.CSS_SELECTOR, "div.prob_num")
            # if int(element.text) == 10:
            #     with open(f"russian_task{TaskNumber.task_number}.json", "a") as file:
            #         json.dump(TaskNumber.all_tasks, file, indent=4,
            #                   ensure_ascii=False)  # закидываем всё в отдельный файл
            #     break
            # with open("test_2.html", "w") as file:
            #     file.write(driver.page_source)

            # actions.move_to_element(element)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


# with open('test.html') as file:
#     src = file.read()


with open("tasks_links_2.json") as file:
    tasks_links = json.load(file)


def get_ids(links):
    url_base = "https://rus-ege.sdamgia.ru"
    while TaskNumber.task_number <= 2:  # проходим по всей длине списка ссылок (пока тестово только 2 номера)
        for task in links.get(str(TaskNumber.task_number)):
            get_source_html(url_base + task)  # забираем каждую ссылку из списка по заданиям
        ids.update({TaskNumber.task_number: tuple(result_links)})  # сохраняем ссылки именно тут, чтобы не обновлялся
        # словарь слишком рано
        result_links.clear()  # очищаем список, чтобы айдишники предыдущего задания не попали в следующее
        print(ids)
        TaskNumber.task_number += 1  # переходим к следующему заданию
    with open("ids.json", "w") as ids_file:
        json.dump(ids, ids_file, indent=4, ensure_ascii=False)


def main():
    get_ids(tasks_links)
    # get_source_html(test_url)


if __name__ == "__main__":
    main()

# dict_task_links = json.loads(tasks_links)
# print(dict_task_links)
