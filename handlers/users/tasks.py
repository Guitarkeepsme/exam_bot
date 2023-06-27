from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message


@dp.message_handler(Command('options'))
async def show_options(message: Message):
    await message.answer(text="Для начала выберите предмет, по которому вы хотите позаниматься.", reply_markup=choice)