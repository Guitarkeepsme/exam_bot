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


print(getting_id("https://rus-ege.sdamgia.ru/problem?id=45326"))




