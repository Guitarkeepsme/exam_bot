from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import subject_callback

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Русский язык', callback_data=subject_callback.new(subject='russian')),
            InlineKeyboardButton(text='Математика', callback_data="choose:math"),
        ],
        [
            InlineKeyboardButton(text='Обществознание', callback_data="choose:social"),
            InlineKeyboardButton(text='Биология', callback_data="choose:biology"),
        ],
        [
            InlineKeyboardButton(text='Физика', callback_data="choose:physics"),
            InlineKeyboardButton(text='Информатика', callback_data="choose:computer"),
        ],
        [
            InlineKeyboardButton(text='История', callback_data="choose:history"),
            InlineKeyboardButton(text='Иностранный язык', callback_data="choose:foreign"),
        ],
        [
            InlineKeyboardButton(text='Химия', callback_data="choose:chemistry"),
            InlineKeyboardButton(text='Литература', callback_data="choose:literature"),
        ],
        [
            InlineKeyboardButton(text='География', callback_data="choose:geography"),
            InlineKeyboardButton(text='Личный кабинет', callback_data='stats')
        ]
    ]
)

