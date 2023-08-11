import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token="5887333260:AAFRvXOC60DQEPmkU1bVyl3teFJp2S7paW0")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define the states
class MenuStates(StatesGroup):
    MAIN_MENU = State()
    SUB_MENU = State()

# Handler for the /start command
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    # Set the initial state
    await MenuStates.MAIN_MENU.set()

    # Display the main menu
    await message.answer("Main Menu", reply_markup=get_main_menu_markup())

# Handler for the main menu buttons
@dp.callback_query_handler(Text(equals=["option1", "option2", "option3"]), state=MenuStates.MAIN_MENU)
async def process_main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    # Get the selected option
    option = callback_query.data

    # Save the selected option in the state
    await state.update_data(selected_option=option)

    # Move to the sub menu state
    await MenuStates.SUB_MENU.set()

    # Display the sub menu
    await callback_query.message.edit_text("Sub Menu", reply_markup=get_sub_menu_markup())

# Handler for the sub menu buttons
@dp.callback_query_handler(Text(equals=["sub_option1", "sub_option2"]), state=MenuStates.SUB_MENU)
async def process_sub_menu(callback_query: types.CallbackQuery, state: FSMContext):
    # Get the selected sub option
    sub_option = callback_query.data

    # Get the selected main option from the state
    data = await state.get_data()
    main_option = data.get("selected_option")

    # Handle the selected options
    await callback_query.answer(f"You selected {main_option} -> {sub_option}")

    # Move back to the main menu state
    await MenuStates.MAIN_MENU.set()

    # Display the main menu
    await callback_query.message.edit_text("Main Menu", reply_markup=get_main_menu_markup())

# Handler for the "back" button
@dp.callback_query_handler(Text(equals=["back"]), state="*")
async def process_back(callback_query: types.CallbackQuery, state: FSMContext):
    # Move back to the previous state
    async with state.proxy() as data:
        previous_state = data.get("previous_state")
        if previous_state:
            await previous_state.set()
            await callback_query.message.edit_text("Back to previous menu")

# Helper function to get the main menu markup
def get_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Option 1", callback_data="option1"),
        InlineKeyboardButton("Option 2", callback_data="option2"),
        InlineKeyboardButton("Option 3", callback_data="option3"),
    )
    return markup

# Helper function to get the sub menu markup
def get_sub_menu_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Sub Option 1", callback_data="sub_option1"),
        InlineKeyboardButton("Sub Option 2", callback_data="sub_option2"),
        InlineKeyboardButton("Back", callback_data="back"),
    )
    return markup

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)