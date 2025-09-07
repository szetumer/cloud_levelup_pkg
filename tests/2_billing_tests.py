import pytest
import json
from pathlib import Path
from src.cloud_levelup.command_files import CommandFile, costmanagement_check, Config
from src.cloud_levelup.parameters import billingexport_config_filepath

@pytest.mark.parametrize(
        "filepath", [
            (billingexport_config_filepath)
        ]
)
class TestMyConfigsStart:
    def test_config_files_exist(self, filepath : Path):
        '''Ensures that you have properly imported your filepaths'''
        assert filepath.exists()
    
    def test_reading_configs_json_file(self, filepath : Path):
        '''Ensures that the json file can be imported correctly'''
        c : Config = Config(filepath)
        assert(isinstance(c.configs, dict))

    def test_reading_configs_json_file(self, filepath : Path):
        '''Ensures that the json file can be imported correctly'''
        c : Config = Config(filepath)
        assert c.configs["billing_account"] is not None


def test_costmanagement_exists():
    r = costmanagement_check.run_commandfile()
    print(r)
    assert r != ""

def test_storage_container_exists():
    l : list = CommandFile.get_storagecontainers_with_account()
    print(l)
    assert len(l) > 0