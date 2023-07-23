from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import time
from loader import getting_id
import asyncio
import aiohttp

# ПОСЛЕ ДОЛГИХ МЫТАРСТВ РЕШИЛ СДЕЛАТЬ ПАРСИНГ ТАКИМ:
# Сначала проходим по странице и парсим айдишники заданий, избегая повторов
# Затем проходим ещё раз, парсим уже сами задания без использования Селениума
# Здесь вырисовывается две проблемы: во-первых, два прохода делать не хотелось бы, а во-вторых,
# пока не понятно, как я буду очищать список, если прошёл все задания
# может быть, сначала загрузить в файл айдишники, а потом уже парсить информацию?


with open("tasks_links_2.json") as links_file:  # открываем файл с ссылками
    tasks_links = json.load(links_file)
with open("ids.json") as id_file:  # открываем файл с ссылками
    ids_f = json.load(id_file)


class TaskNumber:
    task_number = 1
    example_number = 0    # счётчик номеров конкретного задания


# переменные для всех функций
ids = {}
current_ids = []  # сохраняем айдишники конкретного задания, чтобы потом внести их в словарь


def get_page_data():
    pass


def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
    pass


def parse_id(html):
    soup = BeautifulSoup(html, "lxml")
    for task_id in soup.find_all("div", {"class": "problem_container"}, id=True):
        result = task_id.get("id").replace("problem_", "")
        if result not in current_ids:
            current_ids.append(result)


task_content = []  # собираем контент всех примеров конкретного задания
all_tasks_content = {}  # собираем все задания в один словарь, чтобы потом сохранить его


def parse_task(html):
    r = requests.get(html)
    soup = BeautifulSoup(r.text, "lxml")
    TaskNumber.example_number += 1
    current_task_id = getting_id(html)
    head = soup.find("div", class_="pbody")
    if len(head) > 500:  # на случай если в заголовок попадёт теория по заданию
        return None
    head_soup = BeautifulSoup(str(head), "html.parser")
    if head_soup.a:
        return None
    while head_soup.div:
        head_soup.div.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    text = soup.find("div", class_="probtext")
    text_soup = BeautifulSoup(str(text), "html.parser")
    while text_soup.div:
        text_soup.div.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    answer = soup.find("div", class_="solution").find_next_sibling()
    answer_soup = BeautifulSoup(str(answer), "html.parser")
    while answer_soup.div and answer_soup.span:
        answer_soup.div.unwrap()
        answer_soup.span.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    # solution = soup.find("div", {"class": "solution"}).get_text().replace("\u202f", " ").replace("\xa0", " ")
    solution = soup.find("div", {"class": "solution"})
    solution_soup = BeautifulSoup(str(solution), "html.parser")
    while solution_soup.div and solution_soup.span:
        solution_soup.div.unwrap()
        solution_soup.span.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    content = {
        "id": str(current_task_id),
        "head": str(head_soup).replace(" class=\"left_margin\"", "").replace("<p >", "<p>").replace("</p>", "")
                              .replace("</b>", "<b>").replace("\u202f", " ").replace("\xa0", " ")
                              .replace(" align=\"right\"", ""),
        "text": str(text_soup).replace(" class=\"left_margin\"", "").replace("<p >", "<p>").replace("</p>", "")
                              .replace("</b>", "<b>").replace("\u202f", " ").replace("\xa0", " ")
                              .replace(" align=\"right\"", ""),
        "answer": str(answer_soup).replace("Ответ: ", "").replace(" class=\"left_margin\"></p><b><!--rule_info--", "")
                                  .replace("</b>", "<b>").replace("\u202f", " ").replace("\xa0", " ")
                                  .replace("</p>", "")
                                  .replace(" align=\"right\"", ""),
        "solution": str(solution_soup).replace("Пояснение", "").replace(" class=\"left_margin\"", "")
                                      .replace(" class=\"left_margin\"></p><b><!--rule_info--", "").replace("</p>", "")
                                      .replace("</b>", "<b>").replace("\u202f", " ").replace("\xa0", " ")
                                      .replace("<!--rule_info-->", "").replace(" align=\"right\"", "")
    }
    # сделаю небольшое пояснение: я воспользовался методом unwrap и последующим replace, чтобы убрать ненужные мне тэги
    # и метки, но при этом оставить те, что отвечают за преобразование текста. В дальнейшем это будет необходимо,
    # чтобы форматировать сообщения, отправляемые ботом.
    task_content.append(content)
    print(content)


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
        last_height = driver.execute_script("return document.body.scrollHeight")  # запоминаем высоту скролла
        while not reached_page_end:
            time.sleep(2)
            parse_id(driver.page_source)
            scroll_value = 1000
            scroll_by = f'window.scrollBy(0, {scroll_value});'
            driver.execute_script(scroll_by)
            time.sleep(2)
            driver.execute_script(scroll_by)
            new_height = driver.execute_script("return document.body.scrollHeight")  # берём новые данные о высоте
            if last_height == new_height or last_height > 5000:  # проверяем, переместились ли мы до конца
                print("Конец страницы?")
                reached_page_end = True    # заканчиваем
            else:                          # иначе меняем показатель высоты и продолжаем
                last_height = new_height
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_ids(links):
    id_iteration_count = len(tasks_links)
    print(f"Всего заданий: {id_iteration_count}")
    url_base = "https://rus-ege.sdamgia.ru"
    while TaskNumber.task_number <= len(tasks_links):  # проходим по всей длине списка ссылок
        for task in links.get(str(TaskNumber.task_number)):
            get_source_html(url_base + task)  # забираем каждую ссылку из списка по заданиям
        ids.update({TaskNumber.task_number: tuple(current_ids)})  # сохраняем айдишники именно на этом этапе,
        # чтобы словарь не обновлялся слишком рано
        print(ids)
        id_iteration_count -= 1
        print(f"Страница №{TaskNumber.task_number} пройдена, осталось страниц: {id_iteration_count}. "
              f"Количество примеров этого задания: {len(current_ids)}")
        current_ids.clear()  # очищаем список, чтобы айдишники предыдущего задания не попали в следующее
        TaskNumber.task_number += 1  # переходим к следующему заданию
    print("Все ссылки на задания собраны!")
    with open("ids.json", "w") as ids_file:
        json.dump(ids, ids_file, indent=4, ensure_ascii=False)


def get_tasks(task_ids):
    url_base = "https://rus-ege.sdamgia.ru/problem?id="
    while TaskNumber.task_number <= len(tasks_links):
        for task_id in task_ids.get(str(TaskNumber.task_number)):
            parse_task(url_base + str(task_id))
        all_tasks_content.update({TaskNumber.task_number: tuple(task_content)})
        task_content.clear()  # очищаем всё, что собрали по предыдущему заданию, чтобы это не шло на следующее
        print(all_tasks_content)
        TaskNumber.task_number += 1
        if TaskNumber.task_number == len(tasks_links):
            break  # принудительно останавливаем цикл, когда дошли до последнего задания
    # with open("russian_content.json", "w") as content_file:
    #     json.dump(all_tasks_content, content_file, indent=4, ensure_ascii=False)
    with open("russian_content_2.json", "w") as content_file:
        json.dump(all_tasks_content, content_file, indent=4, ensure_ascii=False)


def main():
    # get_ids(tasks_links)  # сначала получаем айдишники всех заданий и сохраняем их
    TaskNumber.task_number = 1  # обнуляем номер задания, чтобы пройтись по ним заново
    get_tasks(ids_f)


if __name__ == "__main__":
    main()