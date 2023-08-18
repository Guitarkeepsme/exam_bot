import logging
from aiogram import Bot, Dispatcher, types
from config import API_TOKEN, host, user, password, db_name
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class Forms(StatesGroup):
    start = State()
    task = State()
    task_answer = State()
    personal_account = State()


bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=MemoryStorage())


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


def getting_answers(example):
    if '|' not in example:
        return [example]
    else:
        return example.split("|")


def getting_id(line):
    number = ''
    for char in line:
        if char.isdigit():
            number += char
        else:
            continue
    return number


def escaping(string):
    markdown_escapes = ['[', ']', '(', ')', '~', '`', '#', '+', '-', '=', '|', '{', '}', '.', '!', ">", "*"]
    # исключил из списка символы >, _ и *, потому что они используются при "первичном" форматировании текстов
    formatted_line = ''
    for char in string:
        if char in markdown_escapes:
            formatted_line += "\\" + char
        else:
            formatted_line += char
    return formatted_line


def formatted(string):
    return string.replace(" class=\"left_margin\"", "").replace("<p >", "\n").replace("</p>", "") \
        .replace("<p>", "\n").replace("</b>", "BOLD").replace("<b>", "BOLD").replace("\u202f", " ") \
        .replace("\xa0", " ").replace(" align=\"right\"", "").replace("</i>", "ITAL").replace("<i>", "ITAL")\
        .replace("<!--auto generated from answers-->", "")\
        .replace("<!--auto generated from answers-->", "").replace("<!--...-->", "")\
        .replace(" <p><span style=\"letter-spacing: 2px;\">", "")\
        .replace(" class=\"left_margin\"", "").replace(" align=\"right\"", "").replace("&lt;...&gt", "<...>")\
        .replace("<!--np-->", "").replace("<b>Прочитайте текст и выполните задания 1−3.<b>", "").replace("Ответ: ", "")\
        .replace(" class=\"left_margin\"></p><b><!--rule_info--", "")\
        .replace(" align=\"right\"", "").replace(" class=\"left_margin\"", "")\
        .replace(" class=\"left_margin\"></p><b><!--rule_info--", "").replace("<!--rule_info-->", "")\
        .replace("<p><b> (см. также Правило ниже). <b>", "").replace("<b>Пояснение (см. также Правило ниже). <b>", "")\
        .replace('<br/><br/>', '').replace("</td>", "").replace("&lt;", "").replace("b&gt;", "BOLD")\
        .replace('style="text-align:center;width:45px"', '').replace('style="height:14px"', '')\
        .replace("<td >A<td >Б<td >В<td >Г<td >Д<td > <td > <td > <td > <td >", "А Б В Г Д")\
        .replace("<td >A<td >Б<td >В<td >Г<td > <td > <td > <td >", "А Б В Г")\
        .replace("Приведём верное соответствие : ", "").replace("<td style=\"margin:auto;border:0", "")\
        .replace("&amp;nbsp", " ")


def parse_modding(string):
    return string.replace("<p>", "\n").replace("BOLD", "*").replace("ITAL", "_") \
        .replace("<td style=\"margin:auto;border:0", "").replace("None", "").replace(" style=\"text-align:right\"", "")\
        .replace("<td \>A<td \>Б<td \>В<td \>Г<td \> <td \> <td \> <td \>", "А Б В Г").replace("<!-- --", "") \
        .replace("&amp;nbsp", " ").replace("<td >", "").replace("<!--", ""). replace("-->", "")\
        # .replace("<td", "").replace(">", "")
