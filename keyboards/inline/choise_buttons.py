from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Русский язык', callback_data=''),
            InlineKeyboardButton(text='Математика', callback_data=''),
        ],
        [
            InlineKeyboardButton(text='Посмотреть свою статистику', callback_data='')
        ]
    ]
)