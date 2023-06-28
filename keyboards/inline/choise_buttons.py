from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import subject_callback

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Русский язык', callback_data=subject_callback.new(subject='russian')),
            InlineKeyboardButton(text='Математика', callback_data="choose:math"),
            # InlineKeyboardButton(text='Обществознание', callback_data=''),
            # InlineKeyboardButton(text='Информатика', callback_data=''),
            # InlineKeyboardButton(text='Биология', callback_data=''),
            # InlineKeyboardButton(text='Физика', callback_data=''),
            # InlineKeyboardButton(text='История', callback_data=''),
            # InlineKeyboardButton(text='Иностранный язык', callback_data=''),
            # InlineKeyboardButton(text='Химия', callback_data=''),
            # InlineKeyboardButton(text='Литература', callback_data=''),
            # InlineKeyboardButton(text='География', callback_data='')
        ],
        [
            InlineKeyboardButton(text='Посмотреть свою статистику', callback_data='next')
        ]
    ]
)

