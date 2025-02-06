from os import getcwd
from os.path import join

from packages.platform_settings import Platform
from packages.app_settings import get_resource_path

class SwissKnifeConfig:

    app_name = "Swiss knife"
    app_source = "swiss_knife.py"
    app_version = "0.2.1"

    screenshot_mac_name = "screenshot_mac.png"
    screenshot_win_name = "screenshot_win.png"
    screenshot_mac_path = f"media/screenshots/{screenshot_mac_name}"
    screenshot_win_path = f"media/screenshots/{screenshot_win_name}"


    png_icon_name = "appicon-sk-rounded.png"
    mac_icon_name = "appicon-sk.icns"
    win_icon_name = "appicon-sk.ico"

    png_icon_path = f"media/icons/{png_icon_name}"
    mac_icon_path = f"media/icons/mac/{mac_icon_name}"
    win_icon_path = f"media/icons/windows/{win_icon_name}"

    build_params = {
        "app_name": app_name,
        "app_version": app_version,
        "screenshot_mac": screenshot_mac_path,
        "screenshot_win": screenshot_win_path,
        "mac_icon_path": mac_icon_path,
        "win_icon_path": win_icon_path,
        "add_data": win_icon_path,
        "app_py": app_source,
    }

    def __init__(self):
        self.icon_path = self.setup_icons_by_platform()

    def setup_icons_by_platform(self) -> str:
        if Platform.PLATFORM == Platform.Windows:
            icon_path = get_resource_path(SwissKnifeConfig.win_icon_name)
        elif Platform.PLATFORM == Platform.macOS:
            icon_path = get_resource_path(SwissKnifeConfig.mac_icon_name)
        return icon_path

class ArchiverConfig:
    pass