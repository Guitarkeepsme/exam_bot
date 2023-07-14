from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import russian_main_callback, rus_task_callback


rus_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Решить пробный вариант ЕГЭ",
                                 callback_data=russian_main_callback.new(option='rus_test'))
        ],
        [
            InlineKeyboardButton(text="Отработать конкретное задание", callback_data='choose:rus_tasks')
        ],
        [
            InlineKeyboardButton(text="Посмотреть статистику по этому предмету", callback_data='choose:rus_stats')
        ]
    ]
)
rus_task = InlineKeyboardMarkup(row_width=4)
task_1 = InlineKeyboardButton(text="1", callback_data=rus_task_callback.new(task="rus_task", number="1"))
task_2 = InlineKeyboardButton(text="2", callback_data=rus_task_callback.new(task="rus_task", number="2"))
task_3 = InlineKeyboardButton(text="3", callback_data=rus_task_callback.new(task="rus_task", number="3"))
task_4 = InlineKeyboardButton(text="4", callback_data=rus_task_callback.new(task="rus_task", number="4"))
task_5 = InlineKeyboardButton(text="5", callback_data=rus_task_callback.new(task="rus_task", number="5"))
task_6 = InlineKeyboardButton(text="6", callback_data=rus_task_callback.new(task="rus_task", number="6"))
task_7 = InlineKeyboardButton(text="7", callback_data=rus_task_callback.new(task="rus_task", number="7"))
task_8 = InlineKeyboardButton(text="8", callback_data=rus_task_callback.new(task="rus_task", number="8"))
task_9 = InlineKeyboardButton(text="9", callback_data=rus_task_callback.new(task="rus_task", number="9"))
task_10 = InlineKeyboardButton(text="10", callback_data=rus_task_callback.new(task="rus_task", number="10"))
task_11 = InlineKeyboardButton(text="11", callback_data=rus_task_callback.new(task="rus_task", number="11"))
task_12 = InlineKeyboardButton(text="12", callback_data=rus_task_callback.new(task="rus_task", number="12"))
task_13 = InlineKeyboardButton(text="13", callback_data=rus_task_callback.new(task="rus_task", number="13"))
task_14 = InlineKeyboardButton(text="14", callback_data=rus_task_callback.new(task="rus_task", number="14"))
task_15 = InlineKeyboardButton(text="15", callback_data=rus_task_callback.new(task="rus_task", number="15"))
task_16 = InlineKeyboardButton(text="16", callback_data=rus_task_callback.new(task="rus_task", number="16"))
task_17 = InlineKeyboardButton(text="17", callback_data=rus_task_callback.new(task="rus_task", number="17"))
task_18 = InlineKeyboardButton(text="18", callback_data=rus_task_callback.new(task="rus_task", number="18"))
task_19 = InlineKeyboardButton(text="19", callback_data=rus_task_callback.new(task="rus_task", number="19"))
task_20 = InlineKeyboardButton(text="20", callback_data=rus_task_callback.new(task="rus_task", number="20"))
task_21 = InlineKeyboardButton(text="21", callback_data=rus_task_callback.new(task="rus_task", number="21"))
task_22 = InlineKeyboardButton(text="22", callback_data=rus_task_callback.new(task="rus_task", number="22"))
task_23 = InlineKeyboardButton(text="23", callback_data=rus_task_callback.new(task="rus_task", number="23"))
task_24 = InlineKeyboardButton(text="24", callback_data=rus_task_callback.new(task="rus_task", number="24"))
task_25 = InlineKeyboardButton(text="25", callback_data=rus_task_callback.new(task="rus_task", number="25"))
task_26 = InlineKeyboardButton(text="26", callback_data=rus_task_callback.new(task="rus_task", number="26"))
task_27 = InlineKeyboardButton(text="27 (Сочинение)", callback_data=rus_task_callback.new(task="rus_task",
                                                                                          number="27"))
rus_task.add(task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_9, task_10, task_11, task_12,
             task_13, task_14, task_15, task_16, task_17, task_18, task_19, task_20)
rus_task.row(task_21, task_22, task_23)
rus_task.row(task_24, task_25, task_26)
rus_task.add(task_27)
