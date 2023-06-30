import logging

from keyboards.inline.choise_buttons import choice
from keyboards.inline.subjects.russian import rus_start, rus_task
from keyboards.inline import callback_data
from loader import dp, Forms, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery


@dp.message_handler(Command('start'))
async def show_options(message: Message):
    await message.answer(text="Для начала выберите предмет, к которому вы будете готовиться:", reply_markup=choice)


@dp.callback_query_handler(text_contains="russian")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer(text="Выберите дальнейшее действие", reply_markup=rus_start)


@dp.callback_query_handler(text_contains="rus_tasks")
async def russian_task_choosing(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer(text="Выберите *номер задания*", reply_markup=rus_task, parse_mode="Markdown")


@dp.callback_query_handler(callback_data.rus_task_callback.filter(task="rus_task"))
async def russian_task(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    number = callback_data.get("number")
    await call.message.answer(text="Минутку, скоро эта функция будет готова, и вы сможете подготовиться к заданию "
                                   "номер " + "*" + str(number) + "*", parse_mode="Markdown")


@dp.callback_query_handler(text_contains="math")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="social")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="biology")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="physics")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="computer")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="history")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="foreign")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="chemistry")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="literature")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text_contains="geography")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Этот раздел пока *в разработке*. Вы можете готовиться к другим предметам.",
                              parse_mode="Markdown")


@dp.callback_query_handler(text="stats")
async def choosing_russian(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("Личный кабинет *в разработке*. Вы можете выбрать один из доступных предметов.",
                              parse_mode="Markdown")


# @dp.callback_query_handler(text="back")
# async def getting_back(message: Message):
#     await message.answer("Хорошо, начнём сначала. Выберите предмет:", reply_markup=choice)
