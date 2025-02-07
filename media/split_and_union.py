import os
from pathlib import Path
import sys
from PIL import Image

current_dir = Path(os.getcwd())
sys.path.append(str(current_dir.joinpath("utils")))
sys.path.append(str(current_dir))


from utils.platform_settings import Platform

class ImageProcessor:
    def __init__(self):
        if Platform.OS == Platform.macOS:
            self.img = 'media/screenshots/screenshot_mac.png'
            self.light_img = 'media/screenshots/screenshot_mac_light.png'
            self.dark_img = 'media/screenshots/screenshot_mac_dark.png'

    def add_suffix_to_filename(self, file_path: str, suffix: str) -> str:
        # Разделите имя файла на путь, имя и расширение
        dir_path = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        # Разделите имя файла на основную часть и расширение
        name, ext = os.path.splitext(filename)

        # Добавьте суффикс к имени файла
        new_name = f"{name}_{suffix}{ext}"

        # Объедините новый путь с новым именем файла
        new_file_path = os.path.join(dir_path, new_name)

        return new_file_path

    def split(self, image_path: str):
        # Загрузите изображение
        img = Image.open(image_path)
        # Получите размеры исходного изображения
        width, height = img.size
        # Рассчитайте середину высоты для разрезания
        mid_width = width // 2
        # Обрежьте левую и правую части
        left_half = img.crop((0, 0, mid_width, height))
        right_half = img.crop((mid_width, 0, width, height))

        name_left = self.add_suffix_to_filename(image_path, "left")
        name_right = self.add_suffix_to_filename(image_path, "right")
        # Сохраните каждую часть как отдельное изображение
        left_half.save(name_left)
        right_half.save(name_right)
        return (name_left, name_right)

    def union(self, image_left: str, image_right: str):
        # Загрузите изображения
        img1 = Image.open(image_left)
        img2 = Image.open(image_right)

        # Объедините изображения по горизонтали
        combined_img = Image.new(img1.mode, (img1.width + img2.width, img1.height))
        combined_img.paste(img1, (0, 0))
        combined_img.paste(img2, (img1.width, 0))

        # Сохраните объединенное изображение
        combined_img.save(self.img)

        self.delete_cache()

    def delete_cache(self):
        files_to_delete = [
            self.add_suffix_to_filename(image_processor.light_img, "left"),
            self.add_suffix_to_filename(image_processor.light_img, "right"),
            self.add_suffix_to_filename(image_processor.dark_img, "left"),
            self.add_suffix_to_filename(image_processor.dark_img, "right"),
        ]

        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Файл {file_path} успешно удален.")
            except FileNotFoundError:
                print(f"Файл {file_path} не найден.")
            except PermissionError:
                print(f"Нет разрешения на удаление файла {file_path}.")
            except Exception as e:
                print(f"Произошла ошибка при удалении файла {file_path}: {e}")

image_processor = ImageProcessor()
img_light = image_processor.split(image_processor.light_img)
img_dark =  image_processor.split(image_processor.dark_img)

image_processor.union(img_light[0], img_dark[1])
