from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os, asyncio
from random import randint
from keyboards import reply_keyboard

load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN")

bot=Bot(BOT_TOKEN)
dp=Dispatcher()


class RadiusState(StatesGroup):
    radius=State()
class MeanState(StatesGroup):
    a=State()
    b=State()
class GuesNumberState(StatesGroup):
    number = State()

class MenuState(StatesGroup):
    first=State()
    second=State()
@dp.message(Command("start"))
async def start(msg: types.Message):
    print(msg.from_user.id, msg.from_user.full_name)
    await msg.answer("привет я бот")

@dp.message(Command("about"))
async def about(msg: types.Message):
    await msg.answer("это бот-напоминатель")

@dp.message(Command("radius"))
async def radius(msg: types.Message, state:FSMContext):
    await msg.answer("введите радиус окружности")
    await state.set_state(RadiusState.radius)

@dp.message(RadiusState.radius)
async def getradius(msg: types.Message, state:FSMContext):
    radius=float(msg.text)
    s=3.14*radius**2
    await msg.answer(f"площадь окружности равна {s}")
    await state.set_state(None)

@dp.message(Command("mean"))
async def mean(msg: types.Message, state:FSMContext):
    await msg.answer("введите первое число")
    await state.set_state(MeanState.a)
@dp.message(MeanState.a)
async def get_a(msg: types.Message, state:FSMContext):
    a=int(msg.text)
    await state.update_data(a=a)
    await msg.answer("введите второе число")
    await state.set_state(MeanState.b)

@dp.message(MeanState.b)
async def get_b(msg: types.Message, state:FSMContext):
    b=int(msg.text)
    data=await state.get_data()
    a=data.get("a")
    sr=(a+b)/2
    await msg.answer(f"среднее равно {sr}")
    await state.set_state(None)

@dp.message(Command("game"))
async def game(msg: types.Message, state:FSMContext):
    number = randint(1,100)
    await state.update_data(number=number, tries=1)
    await msg.answer("я загадал случайное число от 1 до 100, попробуй угадать")
    await state.set_state(GuesNumberState.number)

@dp.message(GuesNumberState.number)
async def get_number(msg: types.Message, state:FSMContext):
    x=int(msg.text)
    data = await state.get_data()
    number = data.get("number")
    tries = data.get("tries")
    if x==number:
        await msg.answer(f"вы угадали за {tries} попыток")
        await state.set_state(None)
    elif x<number:
        await msg.answer("нет, число больше")
        await state.set_state(GuesNumberState.number)
        await state.update_data(tries=tries+1)
    else:
        await msg.answer("нет, число меньше")
        await state.set_state(GuesNumberState.number)
        await state.update_data(tries=tries+1)

@dp.message(Command("menu"))
async def menu(msg: types.Message, state:FSMContext):
    await msg.answer("выберите  первое блюдо",reply_markup=reply_keyboard("борщ", "суп с лапшой", "бульон", "солянка"))
    await state.set_state(MenuState.first)

@dp.message(MenuState.first)
async def first_menu(msg: types.Message, state:FSMContext):
    first=msg.text
    await state.update_data(first=first)
    await msg.answer("выберите  второе блюдо", reply_markup=reply_keyboard("плов", "курица с картошкой", "пельмени", "котлета с рисом"))
    await state.set_state(MenuState.second)


@dp.message(MenuState.second)
async def second_menu(msg: types.Message, state:FSMContext):
    second=msg.text
    await state.update_data(second=second)
    data=await state.get_data()
    first=data.get("first")
    await msg.answer(f"ваш заказ: {first} и {second}")
    await state.set_state(None)












async def main():
    await dp.start_polling(bot)

asyncio.run(main())