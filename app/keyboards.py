from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Текстовый режим', callback_data='text')],
    [InlineKeyboardButton(text='Генерация изображений', callback_data='image')],
    [InlineKeyboardButton(text='Наложение эффектов', callback_data='imageprocessing')]
])

welcome_text = f"""
Привет, это IdeaChat!

Я на все руки мастер: пишу, рисую, объясняю, работаю с файлами. Могу общаться голосовыми сообщениями!

Чтобы я точно понял ваш запрос, закладывайте в него четкие инструкции. Например, начните диалог с глаголов:
• Напиши — составлю текст.
• Объясни — расскажу просто о сложном.
• Нарисуй — создам картинку.
• Придумай — поделюсь идеями.

Порой я могу ошибаться и не понимать ваши просьбы. Но я много учусь, чтобы стать лучше!
"""

effects = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ретро', callback_data='effect_retro)')],
    [InlineKeyboardButton(text='ЧБ', callback_data='effect_black_and_white')]
])