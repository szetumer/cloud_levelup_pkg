import pytest
from pathlib import Path
from parameters import configs_path, private_folderpath

@pytest.mark.parametrize(
        "path", [
         (configs_path)
        ,(private_folderpath)
        ]
)
def test_files_exist(path):
    path.exists()
