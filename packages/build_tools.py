import ast
import subprocess
import sys
from os import getcwd
from pathlib import Path

from jinja2 import Template

current_dir = Path(getcwd())
sys.path.append(str(current_dir))
from config import JinjaTemplates, SwissKnifeConfig
from packages.platform_settings import Platform


def pick_builder_template_by_os(config: SwissKnifeConfig) -> dict:
    if Platform.OS == Platform.Windows:
        params = {
            "app_name": config.build_params["app_name"],
            "win_icon_path": config.build_params["win_icon_path"],
            "app_py": config.build_params["app_py"],
        }
        return {"builder": JinjaTemplates.pyinstaller_win, "params": params}
    elif Platform.OS == Platform.macOS:
        params = {
            "app_name": config.build_params["app_name"],
            "mac_icon_path": config.build_params["mac_icon_path"],
            "app_py": config.build_params["app_py"],
        }
        return {"builder": JinjaTemplates.pyinstaller_mac, "params": params}
    else:
        raise SystemError("Данная ОС на текущий момент не поддерживается!")


def build_with_pyinstaller(config: SwissKnifeConfig) -> None:
    builder_template = pick_builder_template_by_os(config)
    with open(builder_template["builder"], "r") as f:
        template_str = f.read()
        template = Template(template_str)
        command = template.render(builder_template["params"])
        try:
            output = subprocess.check_output(ast.literal_eval(command))
            print(output.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e}")


def build_readme(config: SwissKnifeConfig) -> None:
    with open(JinjaTemplates.readme) as f:
        template_str = f.read()

        template = Template(template_str)
        rendered_md_content = template.render(
            app_name=config.build_params["app_name"],
            app_version=config.build_params["app_version"],
            screenshot_mac=config.build_params["screenshot_mac"],
            screenshot_win=config.build_params["screenshot_win"],
        )

    with open("README.md", "w") as file:
        file.write(rendered_md_content)


if __name__ == "__main__":
    build_readme(SwissKnifeConfig)
    # build_with_pyinstaller(SwissKnifeConfig)
