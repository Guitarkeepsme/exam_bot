import requests
from bs4 import BeautifulSoup
from random import randint

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


sample = "Я написал предложение. Тут есть - всякие ! символы"


def escaping(string):
    markdown_escapes = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    formatted_line = ''
    for char in string:
        if char in markdown_escapes:
            formatted_line += "\\" + char
        else:
            formatted_line += char
    return formatted_line


def getting_answer(example):
    if '|' not in example:
        return example
    else:
        return example.split("|")


def t_list(t_list):
    result = []
    for number in t_list:
        result.append(t_list[number] - 2)
    return result


print(t_list([1, 2, 3, 4, 5]))

