from bs4 import BeautifulSoup
import requests
import re
import unicodedata

# занести в словарь номер задания, вопрос, текст и ответ

url = "https://rus-ege.sdamgia.ru/test?theme=289"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

# headers_list = []
heads_result = []
texts_result = []
answers_result = []
# for headers in soup.find_all("p"):
#     headers_list.append(headers.get("left_margin"))
# task = soup.find("div", {"class": "prob_view"})
heads = soup.find_all("div", {"class": "pbody"}, id=True)
head_counter = 0
text_counter = 0
answer_counter = 0
for head in heads:
    head_counter += 1
    head_line = str(head_counter) + " " + head.find('p', {'class': 'left_margin'}).get_text()
    heads_result.append(head_line)
texts = soup.find_all("div", {"class": "probtext"})
for text in texts:
    text_counter += 1
    text_line = text.find('p', {'class': 'left_margin'}).get_text()
    texts_result.append(text_line)
answers = soup.find_all("div", {"class": "answer"})
for answer in answers:
    answer_counter += 1
    answer_line = str(answer_counter) + " " + answer.find('span').get_text() + " "
    answers_result.append(answer_line)
heads_str = ''.join(heads_result)
texts_str = ''.join(texts_result)
answers_str = ''.join(answers_result)
content = {
    "heads": heads_str,
    "texts": texts_str,
    "answers": answers_str
}
# corrected_head = str(head).replace("</p>", "")
# result_heads.append(task)

# print(content)
print(content)
