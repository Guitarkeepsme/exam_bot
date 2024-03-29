import random
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import time
from loader import getting_id, formatted


# ПОСЛЕ ДОЛГИХ МЫТАРСТВ РЕШИЛ СДЕЛАТЬ ПАРСИНГ ТАКИМ:
# Сначала проходим по странице и парсим айдишники заданий, избегая повторов
# Затем проходим ещё раз, парсим уже сами задания без использования Селениума
# Здесь вырисовывается две проблемы: во-первых, два прохода делать не хотелось бы, а во-вторых,
# пока не понятно, как я буду очищать список, если прошёл все задания
# может быть, сначала загрузить в файл айдишники, а потом уже парсить информацию?


with open("russian_links_2907.json") as links_file:  # открываем файл со ссылками
    tasks_links = json.load(links_file)
print(len(tasks_links))

with open("ids_mathb_180823.json") as id_file:  # открываем файл с айдишниками
    ids_f = json.load(id_file)


class TaskNumber:
    task_number = 1
    example_number = 0    # счётчик номеров конкретного задания


# переменные для всех функций
ids = {}
current_ids = []  # сохраняем айдишники конкретного задания, чтобы потом внести их в словарь
with open("test_2.html") as html_test:
    test_page = html_test.read()


def parse_id(html):
    r = requests.get(html)
    soup = BeautifulSoup(r.text, "lxml")
    rubbish_ids = []
    all_ids = []
    # Да, это очень криво, но пока лень исправлять. Итак, сначала берём все задания:
    for prob in soup.find_all("div", class_="prob_list"):
        # Если в родителе есть "экспанд", это значит, что это другое задание блока, такое нам не нужно
        if 'expand' in prob.parent.get('class'):
            for task_id in prob.find_all("span", class_="prob_nums"):
                # Добавляем его в специальный список
                rubbish_ids.append(task_id.find("a").get_text())
        else:
            for task_id in prob.find_all("span", class_="prob_nums"):
                # Затем остальные (и почему-то ненужные тоже) закидываем в другой список
                result = task_id.find("a").get_text()
                all_ids.append(result)
    # Ну и после этого сравниваем два списка и убираем те айдишники, которые есть в списке ненужных
    for this_id in all_ids:
        if this_id not in rubbish_ids:
            current_ids.append(this_id)


task_content = []  # собираем контент всех примеров конкретного задания
all_tasks_content = {}  # собираем все задания в один словарь, чтобы потом сохранить его

#  ПОКА НЕ ЗНАЮ, ЧТО ДЕЛАТЬ С ТАБЛИЦАМИ И КАК ИХ ПРЕОБРАЗОВЫВАТЬ В ТЕКСТ ПРИ ПАРСИНГЕ


def parse_task(html):
    r = requests.get(html)
    soup = BeautifulSoup(r.text, "lxml")
    TaskNumber.example_number += 1
    # print("Номер " + str(TaskNumber.example_number))
    current_task_id = getting_id(html)
    divs = soup.find_all('div', class_='pbody')
    # print(current_task_id)
    # На некоторых страницах встречаются скрытые куски (как их назвать?)
    # с теорией по заданию и прочим мусором по тому же тэгу с тем же классом, но без id. Поэтому пришлось поиском
    # отсортировать их так, чтобы они парсились только при наличии id
    head_list = []
    for div in divs:
        if div.has_attr('id'):
            head_soup = BeautifulSoup(str(div), "html.parser")
            while head_soup.table:
                head_soup.table.unwrap()
                head_soup.tr.unwrap()
            while head_soup.center:
                head_soup.center.unwrap()
            while head_soup.tr:
                head_soup.tr.unwrap()
            while head_soup.span:
                head_soup.span.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
            while head_soup.div:
                head_soup.div.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
            head_list.append(head_soup)  # возвращаем в виде списка (костыль, ну и ладно)
            break
        else:
            continue
    head_str = ''
    for el in head_list:      # преобразуем список в строку
        head_str += str(el)

    text = soup.find("div", class_="probtext")
    text_soup = BeautifulSoup(str(text), "html.parser")
    while text_soup.center:
        text_soup.center.unwrap()
    while text_soup.span:
        text_soup.span.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    while text_soup.div:
        text_soup.div.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    while text_soup.a:
        text_soup.a.decompose()

    answer = soup.find("div", class_="solution").find_next_sibling()
    answer_soup = BeautifulSoup(str(answer), "html.parser")
    while answer_soup.div:
        answer_soup.div.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    while answer_soup.span:
        answer_soup.span.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    solution = soup.find("div", class_="solution")
    solution_soup = BeautifulSoup(str(solution), "html.parser")

    for div in solution_soup.select("div.wtooltip"):
        div.decompose()  # это для 8 задания, чтобы не забиралась вся информация о правилах
    while solution_soup.div:
        solution_soup.div.unwrap()  # вручную убираем все ненужные тэги, чтобы остались b, i и p
    while solution_soup.span:
        solution_soup.span.decompose()  # под этим тэгом идёт ответ, который нам не нужен
    while solution_soup.a:
        solution_soup.a.decompose()
    while solution_soup.table:
        solution_soup.table.decompose()
    while solution_soup.td:
        solution_soup.td.decompose()
    # while solution_soup.td:
    #     pass
    content = {
        "id": str(current_task_id),
        "head": formatted(head_str),
        "text": formatted(str(text_soup)),
        "answer": formatted(str(answer_soup)),
        "solution": formatted(str(solution_soup))
    }
    # Небольшое пояснение: я воспользовался методом unwrap и последующим replace, чтобы убрать ненужные мне тэги
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
            time.sleep(1)
            scroll_value = random.randint(800, 1500)
            scroll_by = f'window.scrollBy(0, {scroll_value});'
            driver.execute_script(scroll_by)
            # time.sleep(2)
            # driver.execute_script(scroll_by)
            new_height = driver.execute_script("return document.body.scrollHeight")  # берём новые данные о высоте
            time.sleep(2)
            if last_height == new_height:  # проверяем, переместились ли мы до конца
                print(last_height)
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
    id_iteration_count = len(links)
    print(f"Всего заданий: {id_iteration_count}")
    url_base = "https://mathb-ege.sdamgia.ru"
    for link in links.values():
        parse_id(url_base + link)

    # while TaskNumber.task_number <= len(links):  # проходим по всей длине списка ссылок
    #     for task in links.get(str(TaskNumber.task_number)):
    #         parse_id(url_base + task)  # забираем каждую ссылку из списка по заданиям
    #         # get_source_html(url_base + task)  # это уже не актуально
    #         print(task)
        ids.update({TaskNumber.task_number: tuple(current_ids)})  # сохраняем айдишники именно на этом этапе,
        # чтобы словарь не обновлялся слишком рано
        # print(ids)
        id_iteration_count -= 1
        print(f"Страница №{TaskNumber.task_number} пройдена, осталось страниц: {id_iteration_count}. "
              f"Количество примеров этого задания: {len(current_ids)}")
        current_ids.clear()  # очищаем список, чтобы айдишники предыдущего задания не попали в следующее
        TaskNumber.task_number += 1  # переходим к следующему заданию
    print("Все ссылки на задания собраны!")
    with open("ids_mathb_180823.json", "w") as ids_file:
        json.dump(ids, ids_file, indent=4, ensure_ascii=False)


def get_tasks(task_ids):
    url_base = "https://rus-ege.sdamgia.ru/problem?id="
    while TaskNumber.task_number <= len(tasks_links) + 1:
        print("Задание № " + str(TaskNumber.task_number))
        for task_id in task_ids.get(str(TaskNumber.task_number)):
            parse_task(url_base + str(task_id))
        all_tasks_content.update({TaskNumber.task_number: tuple(task_content)})
        task_content.clear()  # очищаем всё, что собрали по предыдущему заданию, чтобы это не шло на следующее
        # print(all_tasks_content)
        TaskNumber.task_number += 1
        if TaskNumber.task_number == len(tasks_links) + 1:
            break  # останавливаем цикл, когда прошли все задания
    # with open("russian_content.json", "w") as content_file:
    #     json.dump(all_tasks_content, content_file, indent=4, ensure_ascii=False)
    with open("rus_content_140823.json", "w") as content_file:
        json.dump(all_tasks_content, content_file, indent=4, ensure_ascii=False)


def main():
    get_ids(tasks_links)  # сначала получаем айдишники всех заданий и сохраняем их
    TaskNumber.task_number = 1  # обнуляем номер задания, чтобы пройтись по примерам задания заново
    # get_tasks(ids_f)


if __name__ == "__main__":
    main()
