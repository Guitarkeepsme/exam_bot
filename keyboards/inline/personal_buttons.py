from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_data import personal_account_callback
personal_account = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Русский язык',
                                 callback_data=personal_account_callback.new(subject='russian_stats')),
            InlineKeyboardButton(text='Математика', callback_data="math"),
        ],
        [
            InlineKeyboardButton(text='Обществознание', callback_data="social"),
            InlineKeyboardButton(text='Биология', callback_data="biology"),
        ],
        [
            InlineKeyboardButton(text='Физика', callback_data="physics"),
            InlineKeyboardButton(text='Информатика', callback_data="computer"),
        ],
        [
            InlineKeyboardButton(text='История', callback_data="history"),
            InlineKeyboardButton(text='Иностранный язык', callback_data="foreign"),
        ],
        [
            InlineKeyboardButton(text='Химия', callback_data="chemistry"),
            InlineKeyboardButton(text='Литература', callback_data="literature"),
        ],
        [
            InlineKeyboardButton(text='География', callback_data="geography"),
            InlineKeyboardButton(text='Назад в меню', callback_data="menu")
        ]
    ]
)