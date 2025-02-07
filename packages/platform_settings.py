import platform


class Platform:
    macOS = "Darwin"
    Windows = "Windows"
    Linux = "Linux"

    OS = platform.system()
