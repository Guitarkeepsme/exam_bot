import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create a bot instance
bot = Bot(token='5887333260:AAFRvXOC60DQEPmkU1bVyl3teFJp2S7paW0')
dispatcher = Dispatcher(bot)

# Define the available subjects, task types, and tasks
SUBJECTS = ['Mathematics', 'Physics']
TASK_TYPES = ['Type 1', 'Type 2', 'Type 3']
TASKS_PER_TYPE = 20

tasks = {
    'Mathematics': {
        'Type 1': [f'Math Task 1-{i}' for i in range(1, TASKS_PER_TYPE + 1)],
        'Type 2': [f'Math Task 2-{i}' for i in range(1, TASKS_PER_TYPE + 1)],
        'Type 3': [f'Math Task 3-{i}' for i in range(1, TASKS_PER_TYPE + 1)]
    },
    'Physics': {
        'Type 1': [f'Physics Task 1-{i}' for i in range(1, TASKS_PER_TYPE + 1)],
        'Type 2': [f'Physics Task 2-{i}' for i in range(1, TASKS_PER_TYPE + 1)],
        'Type 3': [f'Physics Task 3-{i}' for i in range(1, TASKS_PER_TYPE + 1)]
    }
}

# Store the current subject, task type, and task index for each user
user_data = {}


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    # Clear the user's task progress
    user_data.pop(message.chat.id, None)

    # Create the inline keyboard for subject selection
    keyboard = InlineKeyboardMarkup(row_width=2)
    for subject in SUBJECTS:
        callback_data = f'subject:{subject}'
        keyboard.add(InlineKeyboardButton(subject, callback_data=callback_data))

    await message.reply('Select a subject:', reply_markup=keyboard)


@dispatcher.callback_query_handler(lambda query: query.data.startswith('subject:'))
async def select_subject(callback_query: types.CallbackQuery):
    # Extract the selected subject from the callback data
    subject = callback_query.data.split(':')[1]

    # Store the selected subject for the user
    user_data[callback_query.from_user.id] = {'subject': subject, 'type': None, 'task_index': None}

    # Send the task type selection
    await send_task_type_selection(callback_query.from_user.id)


@dispatcher.callback_query_handler(lambda query: query.data.startswith('task_type:'))
async def select_task_type(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id

    # Extract the selected task type from the callback data
    task_type = callback_query.data.split(':')[1]

    # Store the selected task type for the user
    user_data[chat_id]['type'] = task_type

    # Send the first task
    await send_task(chat_id)


@dispatcher.message_handler(lambda message: message.text.startswith('Task'))
async def check_answer(message: types.Message):
    chat_id = message.chat.id

    # Get the user's current task
    current_task = user_data.get(chat_id)
    if not current_task:
        await message.reply('Please select a subject and task type first.')
        return

    # Get the subject, task type, and task index
    subject = current_task['subject']
    task_type = current_task['type']
    task_index = current_task['task_index']

    # Check the user's answer
    if message.text == tasks[subject][task_type][task_index]:
        await message.reply('Correct answer!')
    else:
        await message.reply('Wrong answer. Try again.')
        return

    # Send the next task
    await send_task(chat_id)


@dispatcher.callback_query_handler(lambda query: query.data == 'back_to_subject')
async def go_back_to_subject(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id

    # Clear the user's current task and type
    user_data.pop(chat_id, None)

    # Send the subject selection keyboard again
    keyboard = InlineKeyboardMarkup(row_width=2)
    for subject in SUBJECTS:
        callback_data = f'subject:{subject}'
        keyboard.add(InlineKeyboardButton(subject, callback_data=callback_data))

    await bot.send_message(chat_id, 'Select a subject:', reply_markup=keyboard)


async def send_task_type_selection(chat_id):
    # Create the inline keyboard for task type selection
    keyboard = InlineKeyboardMarkup(row_width=2)
    for task_type in TASK_TYPES:
        callback_data = f'task_type:{task_type}'
        keyboard.add(InlineKeyboardButton(task_type, callback_data=callback_data))

    await bot.send_message(chat_id, 'Select a task type:', reply_markup=keyboard)


async def send_task(chat_id):
    # Get the user's current task
    current_task = user_data.get(chat_id)
    if not current_task:
        return

    # Get the subject, task type, and task index
    subject = current_task['subject']
    task_type = current_task['type']
    task_index = current_task['task_index']

    # Generate a new task index if not set
    if task_index is None:
        task_index = random.randint(0, TASKS_PER_TYPE - 1)
        user_data[chat_id]['task_index'] = task_index

    # Send the task
    await bot.send_message(chat_id, tasks[subject][task_type][task_index])


if __name__ == '__main__':
    executor.start_polling(dispatcher)
