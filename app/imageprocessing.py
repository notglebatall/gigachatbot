import subprocess


def apply_bw_filter(input_path, output_path):
    command = [
        'convert', input_path,  # используем 'convert' вместо 'magick.exe'
        '-colorspace', 'Gray',
        output_path
    ]
    subprocess.run(command, check=True)


def apply_highlight_filter(input_path, output_path):
    command = [
        'convert',
        input_path,
        # Температура и Оттенок
        '-colorspace', 'RGB',
        '-fuzz', '10%',  # изменяет "фокус" для тонкого управления цветовыми изменениям
        # Экспозиция (Экспонир)
        '-brightness-contrast', '10x0',  # +1.05 экспозиция (примерно)
        # Контрастность
        '-brightness-contrast', '0x-5',
        # Светлые области и Тени - можно с помощью "-level" но сложно полностью аналогично
        '-level', '0%,45%,1.0',  # это сильно изменяет светлые области и тени
        # Затемнение (можно изменять яркость минус выражением)
        '-fill', 'black',
        '-colorize', '13',
        # Четкость
        '-sharpen', '0x1.5',
        # Красочность (больше насыщенность)
        '-modulate', '100,110,100',  # второе число увеличивает насыщенность
        output_path
    ]

    subprocess.run(command, check=True)


def apply_city_filter(input_path, output_path):
    command = [
        'convert', input_path,
        '-modulate', '120,100,100',
        '-sigmoidal-contrast', '3x50%',
        '-sharpen', '0x1',
        '-attenuate', '0.5', '+noise', 'Gaussian',
        output_path
    ]
    subprocess.run(command, check=True)


def apply_night_filter(input_path, output_path):
    command = [
        'convert', input_path,
        '-modulate', '80,50,100',
        '-fill', 'blue', '-colorize', '30%',
        '-gamma', '0.7',
        '-contrast',
        output_path
    ]
    subprocess.run(command, check=True)


def apply_pastel_filter(input_path, output_path):
    command = [
        'convert', input_path,
        '-modulate', '110,80,90',
        '-fill', 'lavender', '-colorize', '15%',
        '-brightness-contrast', '-10x10',
        '-blur', '0x1',
        output_path
    ]
    subprocess.run(command, check=True)


def apply_retro_filter(input_path, output_path):
    command = [
        'convert', input_path,
        '-sepia-tone', '60%',
        '-modulate', '100,50,100',
        '-contrast', '-contrast',
        '-noise', '5',
        output_path
    ]
    subprocess.run(command, check=True)
