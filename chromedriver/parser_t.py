from sdamgia import SdamGIA
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage


sdamgia = SdamGIA()
subject = 'rus'
request = 'задание 1'


print(sdamgia.get_catalog(subject=subject))
# # print(sdamgia.get_problem_by_id(subject=subject, id=7))
# print(sdamgia.get_category_by_id(subject=subject, categoryid='354'))
print(sdamgia.get_problem_by_id(subject=subject, id='38778').get('condition').get('text'))