import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

current_dir = Path(os.getcwd())
sys.path.append(str(current_dir.joinpath("packages")))
sys.path.append(str(current_dir))

from config import SwissKnifeConfig
from packages.platform_settings import Platform


def create_icons_for_win(
    input_png_path: str,
    output_ico_path: str,
    sizes: list[tuple] = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)],
):
    # Открываем изображение
    img = Image.open(input_png_path)
    # Сохраняем в формате ICO
    img.save(output_ico_path, format="ICO", sizes=sizes)


def create_icons_for_mac(input_png_path: str, output_ico_path: str):
    """Создать набор иконок для macOS из png"""

    def create_iconset_from_png(png_path: str, iconset_dir: str):
        """Создать набор иконок для Windows из png"""
        # Открываем изображение
        img = Image.open(png_path)

        # Размеры для иконок
        sizes = [16, 32, 64, 128, 256, 512, 1024]

        # Создаем изображения разных размеров
        for size in sizes:
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            resized_img.save(os.path.join(iconset_dir, f"icon_{size}x{size}.png"))

            # Для Retina-дисплеев (2x)
            resized_img_2x = img.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
            resized_img_2x.save(os.path.join(iconset_dir, f"icon_{size}x{size}@2x.png"))

    # Создаем временную папку .iconset
    iconset_dir = os.path.splitext(output_ico_path)[0] + ".iconset"
    os.makedirs(iconset_dir, exist_ok=True)

    # Создаем изображения разных размеров
    create_iconset_from_png(input_png_path, iconset_dir)

    # Конвертируем .iconset в .icns
    subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", output_ico_path])

    # Удаляем временную папку .iconset
    subprocess.run(["rm", "-rf", iconset_dir])


if __name__ == "__main__":
    if Platform.OS == Platform.Windows:
        create_icons_for_win(
            input_png_path=SwissKnifeConfig.png_icon_path,
            output_ico_path=SwissKnifeConfig.win_icon_path,
        )
    elif Platform.OS == Platform.macOS:
        create_icons_for_mac(
            input_png_path=SwissKnifeConfig.png_icon_path,
            output_ico_path=SwissKnifeConfig.mac_icon_path,
        )
