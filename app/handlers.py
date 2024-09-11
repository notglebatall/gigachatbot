import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.generators import generate, gigabot
from app.keyboards import welcome_text, start
from app.generators import get_image

router = Router()


class Generate(StatesGroup):
    text = State()


class Talk(StatesGroup):
    text = State()
    img = State()


@router.message(CommandStart())
async def hello(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=welcome_text, reply_markup=start)


@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ваш предыдущий запрос еще в обработке')


@router.callback_query(F.data == 'text')
async def text_mode(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Talk.text)
    await callback.message.answer('Вы перешли в текстовый режим! Напишите свое сообщение.')


@router.message(Command('text'))
async def text_mode_2(message: Message, state: FSMContext):
    await state.set_state(Talk.text)
    await message.answer('Вы перешли в текстовый режим! Напишите свое сообщение.')


@router.callback_query(F.data == 'image')
async def image_mode(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Talk.img)
    await callback.message.answer('Вы перешли в режим генерации картинок! Напишите свой запрос.')


@router.message(Command('img'))
async def image_mode_2(message: Message, state: FSMContext):
    await state.set_state(Talk.img)
    await message.answer('Вы перешли в режим генерации картинок! Напишите свой запрос.')


@router.message(Talk.text)
async def giga_response(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    waiting_message = await message.answer('Генерирую ответ...')
    response = await generate(model=gigabot, text=message.text)
    await waiting_message.delete()
    await state.clear()
    await message.answer(response)


@router.message(Talk.img)
async def fusion_brain(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    waiting_message = await message.answer('Генерирую картинку...')

    image_number = get_image(url=os.getenv('FB_URL'), api_key=os.getenv('FB_API_KEY'),
                             secret_key=os.getenv('FB_SECRET_KEY'),
                             text=message.text)

    if image_number == -1:
        await message.answer(text="An error occurred while generating")

    else:
        img = FSInputFile(path=f'images/image{image_number}.jpg')

        await waiting_message.delete()
        await state.clear()

        await message.answer_photo(photo=img)

        os.remove(f'images/image{image_number}.jpg')
