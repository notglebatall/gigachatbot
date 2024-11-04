import os
import random
import string

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, BufferedInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.generators import generate, gigabot
from app.keyboards import welcome_text, start, effects
from app.generators import get_image
from app.imageprocessing import *

router = Router()


class Generate(StatesGroup):
    text = State()


class Talk(StatesGroup):
    text = State()
    img = State()


class Effect(StatesGroup):
    photo = State()


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


@router.callback_query(F.data == 'imageprocessing')
async def request_photo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Effect.photo)
    await callback.message.answer('Пришлите фото, на которое будем накладывать эффект')


@router.message(Command('filters'))
async def request_photo_for_filter(message: Message, state: FSMContext):
    await state.set_state(Effect.photo)
    await message.answer('Пришлите фото, на которое будем накладывать эффект')


@router.message(Effect.photo)
async def handle_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Сообщение не содержит фото. Пожалуйста, отправьте фото.")
        return

    random_code = ''.join(random.choices(string.digits, k=5))

    # Задаем путь для сохранения фото
    file_path = f'uploads/{random_code}.jpg'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Получаем файл
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    await message.bot.download_file(file.file_path, destination=file_path)

    with open(file_path, 'rb') as photo_file:
        input_file = BufferedInputFile(photo_file.read(), filename=file_path)
    await message.answer_photo(photo=input_file, caption='Выберите нужный эффект', reply_markup=effects)

    await state.update_data(path=file_path)


@router.callback_query(F.data == 'effect_bw')
async def perform_effect_bw(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    input_path = data['path']
    output_path = input_path.split('/')[0] + '/' + input_path.split('/')[1].split('.')[0] + '_output.jpg'

    apply_bw_filter(input_path, output_path)

    with open(output_path, 'rb') as photo_file:
        output_file = BufferedInputFile(photo_file.read(), filename=output_path)

    await callback.message.answer_photo(photo=output_file)

    try:
        os.remove(output_path)
    except Exception as e:
        print(f"Error deleting files: {e}")


@router.callback_query(F.data == 'effect_night')
async def perform_effect_night(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    input_path = data['path']
    output_path = input_path.split('/')[0] + '/' + input_path.split('/')[1].split('.')[0] + '_output.jpg'

    apply_night_filter(input_path, output_path)

    with open(output_path, 'rb') as photo_file:
        output_file = BufferedInputFile(photo_file.read(), filename=output_path)

    await callback.message.answer_photo(photo=output_file)

    try:
        os.remove(output_path)
    except Exception as e:
        print(f"Error deleting files: {e}")


@router.callback_query(F.data == 'effect_highlight')
async def perform_effect_highlight(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    input_path = data['path']
    output_path = input_path.split('/')[0] + '/' + input_path.split('/')[1].split('.')[0] + '_output.jpg'

    apply_highlight_filter(input_path, output_path)

    with open(output_path, 'rb') as photo_file:
        output_file = BufferedInputFile(photo_file.read(), filename=output_path)

    await callback.message.answer_photo(photo=output_file)

    try:
        os.remove(output_path)
    except Exception as e:
        print(f"Error deleting files: {e}")


@router.callback_query(F.data == 'effect_city')
async def perform_effect_city(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    input_path = data['path']
    output_path = input_path.split('/')[0] + '/' + input_path.split('/')[1].split('.')[0] + '_output.jpg'

    apply_city_filter(input_path, output_path)

    with open(output_path, 'rb') as photo_file:
        output_file = BufferedInputFile(photo_file.read(), filename=output_path)

    await callback.message.answer_photo(photo=output_file)

    try:
        os.remove(output_path)
    except Exception as e:
        print(f"Error deleting files: {e}")


@router.callback_query(F.data == 'effect_pastel')
async def perform_effect_pastel(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    input_path = data['path']
    output_path = input_path.split('/')[0] + '/' + input_path.split('/')[1].split('.')[0] + '_output.jpg'

    apply_pastel_filter(input_path, output_path)

    with open(output_path, 'rb') as photo_file:
        output_file = BufferedInputFile(photo_file.read(), filename=output_path)

    await callback.message.answer_photo(photo=output_file)

    try:
        os.remove(output_path)
    except Exception as e:
        print(f"Error deleting files: {e}")


@router.callback_query(F.data == 'effect_retro')
async def perform_effect_retro(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    input_path = data['path']
    output_path = input_path.split('/')[0] + '/' + input_path.split('/')[1].split('.')[0] + '_output.jpg'

    apply_retro_filter(input_path, output_path)

    with open(output_path, 'rb') as photo_file:
        output_file = BufferedInputFile(photo_file.read(), filename=output_path)

    await callback.message.answer_photo(photo=output_file)

    try:
        os.remove(output_path)
    except Exception as e:
        print(f"Error deleting files: {e}")
