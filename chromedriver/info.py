from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


API_TOKEN = '5887333260:AAFRvXOC60DQEPmkU1bVyl3teFJp2S7paW0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Forms(StatesGroup):
    start = State()


@dp.message_handler(commands="start", state="*")
async def send_welcome(message: types.Message):
    button = InlineKeyboardButton("Выбрать предмет", callback_data='button')
    keyboard = InlineKeyboardMarkup().add(button)
    text = "Привет, " + "*" + message.from_user.first_name + "*! 👋 \n\nЯ помогу вам подготовиться к " \
                                                             "ЕГЭ.""\nДля начала выберите "\
                                                             "предмет, к которому будете готовиться, " \
                                                             "или посмотрите статистику"\
                                                             " своих результатов"
    await Forms.start.set()
    await message.reply(text=text, reply_markup=keyboard,
                        parse_mode='Markdown')


@dp.message_handler(func=lambda c: c.data == 'button')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)