import logging
from keyboards.inline.choise_buttons import choice
from keyboards.inline.subjects.russian import rus_start, rus_task
from keyboards.inline import callback_data
from loader import dp, Forms, FSMContext, getting_answer, escaping
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from data.tasks_content import json_imports
from random import randint

# РЕАЛИЗОВАТЬ СОСТОЯНИЯ, В ПЕРВУЮ ОЧЕРЕДЬ ДЛЯ ПРОХОДОВ ПО ВЫПОЛНЕНИЮ ЗАДАНИЙ
# ПЕРЕПАРСИТЬ ЗАДАНИЯ, ДОБАВИВ АЙДИ, РАЗДЕЛИВ ВАРИАНТЫ ОТВЕТА И СДЕЛАВ ТАК, ЧТОБЫ В ТЕКСТЕ ЗАДАНИЯ НУЖНЫЕ ЭЛЕМЕНТЫ
# БЫЛИ ВЫДЕЛЕНЫ ЛИБО ЖИРНЫМ ШРИФТОМ, ЛИБО КУРСИВОМ


@dp.message_handler(Command('start'), state='*')
async def show_options(message: Message):
    await Forms.start.set()
    await message.answer(text="Для начала выберите предмет, к которому вы будете готовиться:", reply_markup=choice)


@dp.callback_query_handler(text_contains="russian", state=Forms.start)
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_russian = call.data
    logging.info(f"call = {callback_data_russian}")
    await Forms.task.set()
    await call.message.answer(text="Выберите дальнейшее действие", reply_markup=rus_start)


@dp.callback_query_handler(text_contains="rus_tasks", state=Forms.task)
async def russian_task_choosing(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_rus_tasks = call.data
    logging.info(f"call = {callback_data_rus_tasks}")
    await call.message.answer(text="Выберите *номер задания*", reply_markup=rus_task)


@dp.callback_query_handler(callback_data.rus_task_callback.filter(task="rus_task"), state=Forms.task)
async def russian_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    number = callback_data.get("number")
    all_tasks = (json_imports.rus_content.get(number))
    print(len(all_tasks))
    random_task = all_tasks[randint(0, len(all_tasks))]
    print(random_task)
    task_head = str(random_task.get("head")).replace("<p>", "\n").replace("None", "")\
        .replace("<b>", "*").replace("<i>", "ITALICS")

    task_text = str(random_task.get("text")).replace("<p>", "\n").replace("None", "")\
        .replace("<b>", "*").replace("</i>", "ITALICS").replace("<i>", "ITALICS")
    async with state.proxy() as task:
        task['russian'] = random_task  # сохраняем данные в машину состояний

    await Forms.task_answer.set()
    await call.message.answer(text="__Задание " + str(number) + "__"
                              + escaping(task_head) + "\n" +
                              escaping(task_text) +  # функция escaping нужна для того,
                              # чтобы экранировать зарезервированные парсмодом символы
                              "\n\nЗапишите ответ *без пробелов*")


@dp.message_handler(state=Forms.task_answer)
async def russian_task_answer(message: Message, state: FSMContext):
    async with state.proxy() as task:
        answer = getting_answer(task['russian'].get('answer'))  # преобразуем варианты ответа в список
        if message.text.lower() in answer:
            await message.reply("Ответ верен\!")
            await Forms.task.set()
        else:
            await message.reply("Ваш ответ *" + message.text + "*\n\nПравильный ответ: " + "||" +
                                str(task['russian'].get('answer')) + "||", parse_mode="MarkdownV2")
            # по какой-то причине пришлось прописать парсмод, иначе возвращало ошибку
            # получаем ответ из ранее сохранённых данных


# @dp.callback_query_handler(state=rus_task)
# async def russian_task_answer(call: CallbackQuery):
#     await call.answer(cache_time=60)
#     callback_data_russian_task_answer = call.data
#     logging.info(f"call = {callback_data_russian_task_answer}")
#     # await call.message.answer()


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
