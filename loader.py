import logging
from aiogram import Bot, Dispatcher, types
import config
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class Forms(StatesGroup):
    start = State()
    rus_task = State()


bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


def getting_answer(example):
    if '|' not in example:
        return example
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
