from pathlib import Path
from private.configs import ROOT_PATH

rootpath = Path(ROOT_PATH)
testpath = rootpath / "tests"
private_folderpath = rootpath / "private"
configs_path = private_folderpath / "configs.py"