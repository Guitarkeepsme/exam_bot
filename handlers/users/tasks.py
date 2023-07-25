import logging
from keyboards.inline.choise_buttons import choice
from keyboards.inline.subjects import russian
from keyboards.inline import callback_data, personal_buttons
from loader import dp, Forms, FSMContext, getting_answers, escaping
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.tasks_content import json_imports
from random import randint

# РЕАЛИЗОВАТЬ СОСТОЯНИЯ, В ПЕРВУЮ ОЧЕРЕДЬ ДЛЯ ПРОХОДОВ ПО ВЫПОЛНЕНИЮ ЗАДАНИЙ
# ПЕРЕПАРСИТЬ ЗАДАНИЯ, ДОБАВИВ АЙДИ, РАЗДЕЛИВ ВАРИАНТЫ ОТВЕТА И СДЕЛАВ ТАК, ЧТОБЫ В ТЕКСТЕ ЗАДАНИЯ НУЖНЫЕ ЭЛЕМЕНТЫ
# БЫЛИ ВЫДЕЛЕНЫ ЛИБО ЖИРНЫМ ШРИФТОМ, ЛИБО КУРСИВОМ


# Сохраняю прогресс каждого пользователя (в дальнейшем на это будет работать база данных)
user_data = {}


@dp.message_handler(Command('start'), state='*')
async def show_options(message: Message, state: FSMContext):
    await state.finish()  # завершаем все состояния, если они были
    user_data.pop(message.chat.id, None)
    await message.answer(text="Для начала выберите предмет, к которому вы будете готовиться:", reply_markup=choice)


@dp.callback_query_handler(text_contains="russian")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_russian = call.data
    logging.info(f"call = {callback_data_russian}")
    await call.message.answer(text="Хорошо\. Теперь выберите дальнейшее действие", reply_markup=russian.rus_start)


@dp.callback_query_handler(text_contains="rus_tasks", state='*')
async def russian_task_choosing(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.answer(cache_time=60)
    callback_data_rus_tasks = call.data
    logging.info(f"call = {callback_data_rus_tasks}")
    await call.message.answer(text="Выберите *номер задания*", reply_markup=russian.rus_task)


@dp.callback_query_handler(callback_data.rus_task_callback.filter(task="rus_task"))
async def russian_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    number = callback_data.get("number")
    all_tasks = (json_imports.rus_content.get(number))
    print(len(all_tasks))
    random_task = all_tasks[randint(0, len(all_tasks) - 1)]
    task_head = str(random_task.get("head")).replace("*", "\*").replace("<p>", "\n").replace("None", "")\
        .replace("<b>", "*").replace("<i>", "_").replace("</i>", "_").replace("-", "\-").replace(">", "\>")
    task_text = str(random_task.get("text")).replace("*", "\*").replace("<p>", "\n").replace("None", "")\
        .replace("<b>", "*").replace("</i>", "_").replace("<i>", "_").replace("-", "\-").replace(">", "\>")
    async with state.proxy() as task:
        task['solution'] = random_task.get('solution')
        task['number'] = number  # сохраняем номер задания, чтобы пользователь мог отработать другие примеры этого типа
        task['task'] = random_task  # сохраняем все данные в машину состояний
        # task['task_id'] = random_task.get('id')  # добавляем id этого задания, чтобы оно не выпало снова
    await call.message.answer(text="__Задание " + str(number) + "__"
                              + escaping(task_head) + "\n" +
                              escaping(task_text) +  # функция escaping нужна для того,
                              # чтобы экранировать зарезервированные парсмодом символы
                              "\n\nЗапишите ответ *без пробелов*")
    await Forms.task.set()  # переходим в состояние задания


@dp.message_handler(lambda message: message.text, state=Forms.task)
async def task_answer(message: Message, state: FSMContext):
    solution_key = InlineKeyboardMarkup(row_width=2)
    solution_key.add(InlineKeyboardButton('Посмотреть решение', callback_data='solution'))
    async with state.proxy() as task:
        answer = task['task'].get('answer')
        answers = getting_answers(answer)  # преобразуем варианты ответа в список
        if message.text.lower() in answers:
            # await state.finish()  # завершаем состояние
            await message.reply("Ответ верен\!\n\n\nВыберете другое задание или продолжите отрабатывать это?",
                                reply_markup=russian.correct_answer_options)
        else:
            await message.reply("Ваш ответ *" + message.text + "*\n\nПравильный ответ: " + "||" +
                                str(answers) + "||",
                                reply_markup=solution_key)  # а если ответ неверен, оставляем прежнее состояние


@dp.callback_query_handler(text_contains='another_task', state=Forms.task)
async def another_task(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as task:
        current_number = task['number']
    callback_data = {"number": current_number}
    await russian_task(call, callback_data, state)


@dp.callback_query_handler(text='solution', state=Forms.task)
async def get_solution(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as task:
        solution = task['solution']
    solution_parsed = str(solution).replace("*", "\*").replace("<p>", "\n").replace("None", "")\
        .replace("<b>", "*").replace("<i>", "_").replace("</i>", "_").replace(".", "\.")
    await call.message.answer(solution_parsed)


@dp.callback_query_handler(text_contains='to_subjects', state='*')
async def to_subjects(call: CallbackQuery, state: FSMContext):
    await show_options(call.message, state)


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
async def stats(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data_stats = call.data
    logging.info(f"call = {callback_data_stats}")
    await Forms.personal_account.set()  # переходим в состояние личного кабинета
    await call.message.answer("Выберите предмет, по которому вы хотите "
                              "узнать статистику:", reply_markup=personal_buttons.personal_account)


# @dp.callback_query_handler(text_contains='back_to_menu', state='*')
# async def back_from_stats(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     await show_options(call.message, state)


@dp.callback_query_handler(callback_data.personal_account_callback.filter(subject='russian'),
                           state=Forms.personal_account)
async def personal_account_subject(call: CallbackQuery, callback_data: dict):
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('Назад в меню', callback_data='to_subjects'))
    await call.answer(cache_time=60)
    callback_data_stats = call.data
    logging.info(f"call = {callback_data_stats}")
    subject = callback_data.get('subject')
    await call.message.answer("По предмету " + str(subject) + " будет информация после добавления базы данных",
                              reply_markup=back_button)
# @dp.callback_query_handler(text="back")
# async def getting_back(message: Message):
#     await message.answer("Хорошо, начнём сначала. Выберите предмет:", reply_markup=choice)
