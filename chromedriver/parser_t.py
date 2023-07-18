import requests
from bs4 import BeautifulSoup


html = "<div class='answer' style='display:none'><span style='letter-spacing: 2px;'>Ответ: что</span></div>"

soup = BeautifulSoup(html, "html.parser")
while soup.div:
    soup.div.unwrap()
while soup.span:
    soup.span.unwrap()


def getting_id(line):
    number = ''
    for char in line:
        if char.isdigit():
            number += char
        else:
            continue
    return number


# def parse_task(html):
#     r = requests.get(html)
#     soup = BeautifulSoup(r.text, "lxml")
#     TaskNumber.example_number += 1
#     current_task_id = getting_id(html)
#     print(current_task_id)
#     head = soup.find("div", class_="pbody")
#     if len(head) > 500:  # на случай если в заголовок попадёт теория по заданию
#         return None
#     head_soup = BeautifulSoup(str(head), "html.parser")
#     while head_soup.div:
#         head_soup.div.unwrap()  # вручную убираем все тэги див, чтобы остались b и p
#     text = soup.find("div", class_="probtext")
#     text_soup = BeautifulSoup(str(text), "html.parser")
#     while text_soup.div:
#         text_soup.div.unwrap()  # вручную убираем все тэги див, чтобы остались b и p
#     answer = soup.find("div", class_="solution").find_next_sibling()
#     answer_soup = BeautifulSoup(str(answer), "html.parser")
#     while answer_soup.div and answer_soup.span:
#         answer_soup.div.unwrap()
#         answer_soup.span.unwrap()  # вручную убираем все тэги див, чтобы остались b и p
#     # solution = soup.find("div", {"class": "solution"}).get_text().replace("\u202f", " ").replace("\xa0", " ")
#     solution = soup.find("div", {"class": "solution"})
#     solution_soup = BeautifulSoup(str(solution), "html.parser")
#     while solution_soup.div and solution_soup.span:
#         solution_soup.div.unwrap()
#         solution_soup.span.unwrap()  # вручную убираем все тэги див, чтобы остались b и p
#     content = {
#         "id": current_task_id,
#         "head": head_soup,
#         "text": text_soup,
#         "answer": answer_soup,  # нужно убрать слово "Ответ"
#         "solution": solution_soup  # нужно убрать слово "Пояснение"
#     }
#     task_content.append(content)
#     print(content)




