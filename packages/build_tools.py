import sys
from os import getcwd
from pathlib import Path

from jinja2 import Template

current_dir = Path(getcwd())
sys.path.append(str(current_dir))
from config import SwissKnifeConfig
from platform_settings import Platform

class Templates:
    pybuilder_mac = "pybuilder_mac_template.md.j2"
    pybuilder_win = "pybuilder_win_template.md.j2"



def pick_builder_template_by_os(config: SwissKnifeConfig) -> str:
    if Platform.PLATFORM == Platform.Windows:
        params = {
            config.build_params["app_name"],
            config.build_params["win_icon_path"],
            config.build_params["app_py"],
        }
        return {
            "builder": Templates.pybuilder_win,
            "params": params
        }
    elif Platform.PLATFORM == Platform.macOS:
        params = {
            config.build_params["app_name"],
            config.build_params["mac_icon_path"],
            config.build_params["app_py"],
        }
        return {
            "builder": Templates.pybuilder_mac,
            "params": params
        }
    else:
        raise SystemError("Данная ОС на текущий момент не поддерживается!")


def build_pybuilder(config: SwissKnifeConfig) -> str:

    builder_template = pick_builder_template_by_os(config)
    with open(builder_template["builder"], "r") as f:
        template_str = f.read()

        template = Template(template_str)
        return template.render(
            builder_template["params"]
        )


def build_readme(config: SwissKnifeConfig) -> None:
    with open("templates/readme_template.md.j2", "r") as f:
        template_str = f.read()

        template = Template(template_str)
        rendered_md_content = template.render(
            app_name=config.build_params["app_name"],
            app_version=config.build_params["app_version"],
            screenshot_mac=config.build_params["screenshot_mac"],
            screenshot_win=config.build_params["screenshot_win"],
            mac_icon_path=config.build_params["mac_icon_path"],
            win_icon_path=config.build_params["win_icon_path"],
            add_data=config.build_params["add_data"],
            app_py=config.build_params["app_py"],
        )

    with open("README.md", "w") as file:
        file.write(rendered_md_content)


if __name__ == "__main__":
    build_readme(SwissKnifeConfig)
