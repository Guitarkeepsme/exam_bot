import logging
import os
from keyboards.inline.choise_buttons import choice
from keyboards.inline.subjects.russian import rus_start, rus_task
from keyboards.inline import callback_data
from loader import dp, Forms, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
# from data.tasks_content import json_imports
from random import randint
import json


# РЕАЛИЗОВАТЬ СОСТОЯНИЯ, В ПЕРВУЮ ОЧЕРЕДЬ ДЛЯ ПРОХОДОВ ПО ВЫПОЛНЕНИЮ ЗАДАНИЙ
# ПЕРЕПАРСИТЬ ЗАДАНИЯ, ДОБАВИВ АЙДИ, РАЗДЕЛИВ ВАРИАНТЫ ОТВЕТА И СДЕЛАВ ТАК, ЧТОБЫ В ТЕКСТЕ ЗАДАНИЯ НУЖНЫЕ ЭЛЕМЕНТЫ
# БЫЛИ ВЫДЕЛЕНЫ ЛИБО ЖИРНЫМ ШРИФТОМ, ЛИБО КУРСИВОМ


working_directory = os.getcwd()
rus_path = working_directory + '/data/tasks_content/russian_content.json'

with open(rus_path) as rus_data:
    rus_content = json.load(rus_data)


@dp.message_handler(Command('start'))
async def show_options(message: Message):
    await message.answer(text="Для начала выберите предмет, к которому вы будете готовиться:", reply_markup=choice)


@dp.callback_query_handler(text_contains="russian")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_russian = call.data
    logging.info(f"call = {callback_data_russian}")
    await Forms.rus_task.set()
    await call.message.answer(text="Выберите дальнейшее действие", reply_markup=rus_start)


@dp.callback_query_handler(text_contains="rus_tasks", state=rus_task)
async def russian_task_choosing(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_rus_tasks = call.data
    logging.info(f"call = {callback_data_rus_tasks}")
    await call.message.answer(text="Выберите *номер задания*", reply_markup=rus_task, parse_mode="Markdown")


@dp.callback_query_handler(callback_data.rus_task_callback.filter(task="rus_task"))
async def russian_task(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    number = callback_data.get("number")
    all_tasks = (rus_content.get(str(number)))
    random_task = all_tasks[randint(0, len(number))]
    # async with
    await call.message.answer(text=str(random_task.get("head")) + "\n\n" + str(random_task.get("text")))
    # берём случайное задание из списка


@dp.callback_query_handler(state=rus_task)
async def russian_task_answer(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_russian_task_answer = call.data
    logging.info(f"call = {callback_data_russian_task_answer}")
    # await call.message.answer()


@dp.callback_query_handler(text_contains="math")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_math = call.data
    logging.info(f"call = {callback_data_math}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="social")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_social = call.data
    logging.info(f"call = {callback_data_social}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="biology")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_biology = call.data
    logging.info(f"call = {callback_data_biology}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="physics")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_physics = call.data
    logging.info(f"call = {callback_data_physics}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="computer")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_computer = call.data
    logging.info(f"call = {callback_data_computer}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="history")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_history = call.data
    logging.info(f"call = {callback_data_history}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="foreign")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_foreign = call.data
    logging.info(f"call = {callback_data_foreign}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="chemistry")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_chemistry = call.data
    logging.info(f"call = {callback_data_chemistry}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="literature")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_literature = call.data
    logging.info(f"call = {callback_data_literature}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="geography")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_geography = call.data
    logging.info(f"call = {callback_data_geography}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text="stats")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_stats = call.data
    logging.info(f"call = {callback_data_stats}")
    await call.message.answer("Личный кабинет *в разработке*. Вы можете выбрать один из доступных предметов.",
                              parse_mode="Markdown")


# @dp.callback_query_handler(text="back")
# async def getting_back(message: Message):
#     await message.answer("Хорошо, начнём сначала. Выберите предмет:", reply_markup=choice)
