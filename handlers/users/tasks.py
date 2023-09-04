import logging
from keyboards.inline.choise_buttons import choice
from keyboards.inline.subjects import russian
from keyboards.inline import callback_data, personal_buttons
from loader import dp, Forms, getting_answers, escaping, parse_modding
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.tasks_content import json_imports
from random import randint
from config import connection
from filters import bot_messages


@dp.message_handler(Command('start'))
async def begin(message: Message):
    start_button = InlineKeyboardMarkup()
    start_button.add(InlineKeyboardButton('Начнём!', callback_data='menu'))
    await message.answer(text="Приветствую, *"
                              + message.from_user.first_name + "*\! 👋\n"
                              + bot_messages.start_message, reply_markup=start_button)


@dp.callback_query_handler(text='menu', state='*')
async def show_options(call: CallbackQuery, state: FSMContext):
    await state.finish()  # завершаем все состояния, если они были
    # включаем базу данных и добавляем id
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO users (id) VALUES (%s) ON CONFLICT (id) DO NOTHING', (call.from_user.id,))
        connection.commit()
    await call.message.answer(text="Выберите предмет, к которому вы будете готовиться:", reply_markup=choice)


@dp.callback_query_handler(text_contains="russian_options", state='*')
async def choosing_russian(call: CallbackQuery, state: FSMContext):
    await state.finish()  # завершаем все состояния, если они были
    await call.answer(cache_time=60)
    callback_data_russian = call.data
    logging.info(f"call = {callback_data_russian}")
    await call.message.answer(text="Хорошо\. Теперь выберите дальнейшее действие", reply_markup=russian.rus_start)


@dp.callback_query_handler(text_contains="rus_tasks", state='*')
async def russian_task_choosing(call: CallbackQuery, state: FSMContext):
    await state.finish()  # завершаем все состояния, если они были
    await call.answer(cache_time=60)
    callback_data_rus_tasks = call.data
    logging.info(f"call = {callback_data_rus_tasks}")
    await call.message.answer(text="Выберите *номер задания*", reply_markup=russian.rus_task)


@dp.callback_query_handler(callback_data.rus_task_callback.filter(task="rus_task"))
async def russian_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()  # завершаем состояние, если оно было
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('Назад', callback_data='rus_tasks'))
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    number = callback_data.get("number")
    all_tasks = (json_imports.rus_content.get(number))
    solved = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT problem_id FROM actions WHERE user_id = (%s) AND is_solved = true', (call.from_user.id,))
        cursor.fetchall()
        if cursor.fetchall():
            solved.extend(cursor.fetchall()[0])
        connection.commit()
    random_task = all_tasks[randint(0, len(all_tasks) - 1)]
    # Проверяем, не попалось ли решённое задание снова
    while random_task in solved:
        random_task = all_tasks[randint(0, len(all_tasks) - 1)]
    task_head = escaping(str(random_task.get("head")))
    task_text = escaping(str(random_task.get("text")))
    async with state.proxy() as task:
        task['subject'] = 'russian'
        task['solution'] = random_task.get('solution')
        task['number'] = int(number)  # сохраняем номер задания, чтобы пользователь мог отработать другие примеры
        task['task'] = random_task  # сохраняем все данные в машину состояний
    await call.message.answer(text="__Задание " + str(number) + "__" + parse_modding(task_head))
    await call.message.answer(text=parse_modding(task_text))
    await call.message.answer(text="\n\nЗапишите ответ *без пробелов*", reply_markup=back_button)
    await Forms.task.set()  # переходим в состояние задания

    # "__Задание " + str(escaping(number)) + "__"
    # + escaping(task_head) + "\n" +
    # escaping(task_text) +  # функция escaping нужна для того,
    # # чтобы экранировать зарезервированные парсмодом символы
    # "\n\nЗапишите ответ *без пробелов*"


@dp.message_handler(lambda message: message.text, state=Forms.task)
async def task_answer(message: Message, state: FSMContext):
    solution_key = InlineKeyboardMarkup(row_width=2)
    solution_key.add(InlineKeyboardButton('Посмотреть решение', callback_data='solution'))
    async with state.proxy() as task:
        num = task['number']
        answer = task['task'].get('answer')
        task_id = task['task'].get('id')
        subject = task['subject']
        answers = getting_answers(answer)  # преобразуем варианты ответа в список
        if message.text.lower() in answers:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO actions (problem_id, user_id, subject, number, is_solved) '
                               'VALUES ((%s), (%s), (%s), (%s), true)', (task_id, message.from_user.id, subject, num))
                connection.commit()
            # await state.finish()  # завершаем состояние
            await message.reply("Ответ верен\!\n\n\nВыберете другое задание или продолжите отрабатывать это?",
                                reply_markup=russian.correct_answer_options)
        else:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO actions (problem_id, user_id, subject, number, is_solved) '
                               'VALUES ((%s), (%s), (%s), (%s), false)', (task_id, message.from_user.id, subject, num))
                connection.commit()
            await message.reply("Ваш ответ *" + message.text + "*\n\nПравильный ответ: " + "||" +
                                str(answers) + "||",
                                reply_markup=solution_key)  # а если ответ неверен, оставляем прежнее состояние


@dp.callback_query_handler(text_contains='another_task', state=Forms.task)
async def another_task(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as task:
        current_number = task['number']
    callback_data = {'number': str(current_number)}
    await russian_task(call, callback_data, state)


@dp.callback_query_handler(text='solution', state=Forms.task)
async def get_solution(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as task:
        solution = task['solution']
    solution_parsed = escaping(str(solution))
    await call.message.answer(parse_modding(solution_parsed))


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
    await call.message.answer("Выберите предмет, по которому вы хотите "
                              "узнать статистику:", reply_markup=personal_buttons.personal_account)


# @dp.callback_query_handler(text_contains='back_to_menu', state='*')
# async def back_from_stats(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     await show_options(call.message, state)

# ,
#                            state=Forms.personal_account
@dp.callback_query_handler(callback_data.personal_account_callback.filter(subject='russian_stats'))
async def personal_account_subject(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await Forms.personal_account.set()  # переходим в состояние личного кабинета
    await call.answer(cache_time=60)
    callback_data_stats = call.data
    logging.info(f"call = {callback_data_stats}")
    subject = callback_data.get('subject').replace('_stats', '')
    async with state.proxy() as info:
        info['subject'] = subject
    total_amount = 0  # считаем, сколько всего задач решил пользователь
    total_true = 0
    total_false = 0
    with connection.cursor() as cursor:
        # Забираем информацию о том, сколько всего задач решил пользователь
        cursor.execute('SELECT COUNT (problem_id) FROM actions WHERE user_id = (%s) AND subject = (%s)',
                       (call.from_user.id, subject,))
        current = cursor.fetchall()[0][0]  # почему нужно два нуля???
        total_amount += current
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT (problem_id) FROM actions WHERE user_id = (%s)'
                       ' AND is_solved = true AND subject = (%s)', (call.from_user.id, subject,))
        current_true = cursor.fetchall()[0][0]
        total_true += current_true
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT (problem_id) FROM actions WHERE user_id = (%s)'
                       ' AND is_solved = false AND subject = (%s)', (call.from_user.id, subject,))
        current_false = cursor.fetchall()[0][0]
        total_false += current_false
    await call.message.answer("__Ваша статистика по этому предмету__\n\n\nВсего заданий: *" + str(total_amount)
                              + "*\nИз них решены правильно: *" + str(total_true) + "*\nДопущено ошибок: *"
                              + str(total_false) + "*\n\n\nЕсли вам нужна информация по конкретному заданию, "
                                                   "напишите его номер в ответном сообщении\.",
                              reply_markup=personal_buttons.back_buttons)


@dp.message_handler(state=Forms.personal_account)
async def problem_stats(message: Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as info:
            subject = info['subject']
            false = 0
            true = 0
            total = 0
            with connection.cursor() as cursor:
                cursor.execute('SELECT COUNT (problem_id) FROM actions WHERE user_id = (%s)'
                               'AND is_solved = false AND subject = (%s) AND number = (%s)',
                               (message.from_user.id, subject, int(message.text)))
                current_false = cursor.fetchall()[0][0]
                false += current_false
            with connection.cursor() as cursor:
                cursor.execute('SELECT COUNT (problem_id) FROM actions WHERE user_id = (%s)'
                               'AND is_solved = true AND subject = (%s) AND number = (%s)',
                               (message.from_user.id, subject, int(message.text)))
                current_true = cursor.fetchall()[0][0]
                true += current_true
            with connection.cursor() as cursor:
                cursor.execute('SELECT COUNT (problem_id) FROM actions WHERE user_id = (%s) '
                               'AND subject = (%s) AND number = (%s)',
                               (message.from_user.id, subject, int(message.text)))
                current_total = cursor.fetchall()[0][0]
                total += current_total
            if total == 0:
                await message.answer("Вы ещё *не приступали* к этому заданию или такого задания *не существует*\."
                                     , reply_markup=personal_buttons.back_buttons)
            else:
                await message.answer("__Ваша статистика по этому заданию__\n\n\nВсего примеров: *" + str(total)
                                     + "*\nИз них решены правильно: *" + str(true) + "*\nДопущено ошибок: *"
                                     + str(false) + "*", reply_markup=personal_buttons.back_buttons)
    else:
        await message.answer("Введите номер задания, пожалуйста\.")


@dp.callback_query_handler(callback_data.russian_main_callback.filter(option='rus_test'), state='*')
async def russian_test(call: CallbackQuery, state: FSMContext):
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton('Назад', callback_data='russian_options'))
    await state.finish()
    await call.message.answer("Эта функция ещё в разработке, ждите\.", reply_markup=back_button)

