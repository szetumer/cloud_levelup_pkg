from pathlib import Path
import os

ROOT_PATH = os.getcwd()
rootpath = Path(ROOT_PATH)
testpath = rootpath / "tests"
private_folderpath = rootpath / "private"
configs_path = private_folderpath / "configs.py"