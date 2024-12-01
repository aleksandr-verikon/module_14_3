from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = '7898781198:AAFPcK1g6Er5calmo2EpyvdhYllVPe_3G7w'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
#-----------------------------------------Модуль 14.3----------------------------------------------
button3 = KeyboardButton(text = 'Купить')
kb.add(button1, button2, button3)

products = InlineKeyboardMarkup(resize_keyboard=True)
button_product1 = InlineKeyboardButton('Product1', callback_data="product_buying")
button_product2 = InlineKeyboardButton('Product2', callback_data="product_buying")
button_product3 = InlineKeyboardButton('Product3', callback_data="product_buying")
button_product4 = InlineKeyboardButton('Product4', callback_data="product_buying")
products.add(button_product1, button_product2, button_product3, button_product4)

@dp.message_handler(text = ['Купить'])
async def get_buying_list(message):
    await message.answer('Название: Product1 | Oписание: описание1 | Цена: 100')
    with open("баблгам.jpg", "rb") as babl:
        await message.answer_photo(babl)

    await message.answer('Название: Product2 | Oписание: описание2 | Цена: 200')
    with open("vanil.jpg", "rb") as vanil:
        await message.answer_photo(vanil)

    await message.answer('Название: Product3 | Oписание: описание3 | Цена: 300')
    with open("клубника.jpg", "rb") as klubn:
        await message.answer_photo(klubn)

    await message.answer('Название: Product4 | Oписание: описание4 | Цена: 400')
    with open("fruct_led.jpg", "rb") as fruct:
        await message.answer_photo(fruct)
    await message.answer('Выберите продукт для покупки:', reply_markup=products)

@dp.callback_query_handler(text = ["product_buying"])
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

#------------------------------------------------------------------------------------------------------

dvach = InlineKeyboardMarkup(resize_keyboard=True)
button_dvach1 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_dvach2 = InlineKeyboardButton('Формула расчёта', callback_data='formulas')
dvach.add(button_dvach1, button_dvach2)

@dp.message_handler(text = ['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=dvach)



@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')

    await call.answer()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)


@dp.callback_query_handler(text = ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.age()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    formula = (int(data['growth']) * 6.25) + (int(data['weight']) * 10) - (int(data['age']) * 5)
    await message.answer(f"Ваша норма каллорий: {formula}")

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)