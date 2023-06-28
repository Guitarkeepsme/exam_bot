from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import russian_main_callback


rus_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Решить пробный вариант ЕГЭ",
                                 callback_data=russian_main_callback.new(option='rus_test'))
        ],
        [
            InlineKeyboardButton(text="Отработать конкретное задание",
                                 callback_data=russian_main_callback.new(option='rus_task'))
        ],
        [
            InlineKeyboardButton(text="Посмотреть статистику по этому предмету",
                                 callback_data=russian_main_callback.new(option='rus_stats'))
        ],
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data=russian_main_callback.new(option='back'))
        ]
    ]
)
