import json
import time
import os
import requests
import base64

import random
import string
import logging

from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()

gigabot = GigaChat(
    credentials=os.getenv('GIGACHAT_TOKEN'),
    verify_ssl_certs=False,
    )


async def generate(model, text):
    try:
        response = model.chat(text)
        return response.choices[0].message.content
    except Exception as e:
        return f'Произошла ошибка: {e}'


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    @staticmethod
    def get_number(length=6) -> str:
        all_symbols = string.ascii_uppercase + string.digits
        number = ''.join(random.choice(all_symbols) for _ in range(length))

        return number

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def get_image(url, api_key, secret_key, text):
    api = Text2ImageAPI(url=url, api_key=api_key, secret_key=secret_key)
    model_id = api.get_model()
    uuid = api.generate(prompt=text, model=model_id)
    images = api.check_generation(uuid)

    if images != -1:
        image_base64 = images[0]
        image_data = base64.b64decode(image_base64)
        number = api.get_number()

        # Проверяем, существует ли директория 'images', если нет - создаем ее
        if not os.path.exists('images'):
            os.makedirs('images')

        with open(file=f"images/image{number}.jpg", mode="wb") as file:
            file.write(image_data)

        logging.info(f"Successful generation")
        return number

    return -1
