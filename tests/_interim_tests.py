import pytest
from src.cloud_levelup.command_files import CommandFile
from src.cloud_levelup.parameters import 

def test_get_storageaccount():
    assert "" == CommandFile.get_storageaccount_name()

@pytest.mark.parametrize(
        "filepath", [
            (billingexport_config_filepath)
        ]
)
def test_read_config(filepath):
    pass