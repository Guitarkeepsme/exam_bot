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


bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
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
    markdown_escapes = ['[', ']', '(', ')', '~', '`', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    # исключил из списка символы >, _ и *, потому что они используются при "первичном" форматировании текстов
    formatted_line = ''
    for char in string:
        if char in markdown_escapes:
            formatted_line += "\\" + char
        else:
            formatted_line += char
    return formatted_line


