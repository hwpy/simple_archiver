import platform


class Platform:
    macOS = "Darwin"
    Windows = "Windows"
    Linux ="Linux"

    PLATFORM = platform.system()