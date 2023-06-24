from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboa import Keyboa


API_TOKEN = '5887333260:AAFRvXOC60DQEPmkU1bVyl3teFJp2S7paW0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Forms(StatesGroup):
    start = State()


@dp.message_handler(commands="start", state="*")
async def send_welcome(message: types.Message):
    buttons = ["Выбрать предмет", "Посмотреть статистику"]
    keyboard = Keyboa(items=buttons)
    await Forms.start.set()
    await message.reply("Привет, " + "*" + message.from_user.first_name +
                        "*! 👋 \n\nЯ помогу вам подготовиться к ЕГЭ.""\nДля начала выберите "
                        "предмет, к которому будете готовиться, или посмотрите статистику"
                        " своих результатов", reply_markup=keyboard(),
                        parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)