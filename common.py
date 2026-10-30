from _in_package import *
from config import *


def formatting_path(path: str) -> str:
        path = path.strip()
        path = path.replace("\\", "/")
        if path[-1] != "/":
                path += "/"
        return path