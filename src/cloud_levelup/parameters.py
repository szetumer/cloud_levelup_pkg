from pathlib import Path
import platform
from typing import LiteralString, Literal
import os

ROOT_PATH = os.getcwd()
rootpath = Path(ROOT_PATH)
testspath = rootpath / "tests"
commandspath = rootpath / "commands"
create_costman_export_configpath = rootpath / "my_configs" / "costman_export.json"

def get_system() -> Literal["Windows"] | Literal["iOs"] | Literal["Linux"]:
    if platform.system() == "Windows":
        return "Windows"
    elif platform.system() == "Linux":
        return "Linux"
    elif os.name == "posix":
        return "iOs"
    else:
        raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
