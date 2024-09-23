import subprocess


def apply_bw_filter(input_path, output_path):
    command = [
        'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe', input_path,
        '-colorspace', 'Gray',
        output_path
    ]
    subprocess.run(command, check=True)


def apply_light_brightness_filter(input_path, output_path):
    # Легкое высветление: увеличиваем яркость на 10%
    command = [
        'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe', input_path,
        '-modulate', '110,100,100',  # Яркость: 110%, Насыщенность и Оттенок без изменений
        output_path
    ]
    subprocess.run(command, check=True)


def apply_pastel_filter(input_path, output_path):
    # Пастель: уменьшаем насыщенность и повышаем яркость
    command = [
        'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe', input_path,
        '-modulate', '105,80,100',  # Яркость: 105%, Насыщенность: 80%, Оттенок без изменений
        '-contrast-stretch', '0x5%',  # Повышаем контрастность
        output_path
    ]
    subprocess.run(command, check=True)


def apply_night_filter(input_path, output_path):
    # Ночной эффект: понижаем яркость и добавляем синий оттенок
    command = [
        'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe', input_path,
        '-modulate', '80,80,100',  # Яркость и Насыщенность: 80%
        '-colorize', '20,20,60',   # Добавляем синий оттенок
        output_path
    ]
    subprocess.run(command, check=True)


def apply_retro_filter(input_path, output_path):
    # Ретро эффект: альтернативный вариант
    command = [
        'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe', input_path,
        '-sepia-tone', '70%',      # Применяем сепию
        '-grain', '10',            # Добавляем зернистость
        '-vignette', '0x1',        # Добавляем виньетку
        output_path
    ]
    subprocess.run(command, check=True)
