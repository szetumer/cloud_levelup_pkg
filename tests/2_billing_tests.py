import pytest
import json
from pathlib import Path
from src.cloud_levelup.command_files import Command, costmanagement_check, Config, GetAzure
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

class TestCorrectBillingAccountAndProfileInformation:
    
    @pytest.fixture(scope="class")
    def config(self) -> Config:
        c : Config = Config(billingexport_config_filepath)
        return c
    
    def test_you_have_added_anything_in_the_billing_account(self, config : Config):
        '''Ensures that the json file can be imported correctly'''
        assert config.configs["billing_account"] is not None

    def test_added_legit_billing_account(self, config : Config):
        s : str = config.configs["billing_account"]
        b_accounts = GetAzure.billing_account_names()
        assert s in b_accounts

    def test_added_anything_to_billing_profile(self, config : Config):
        s : str = config.configs["billing_profile"]
        assert(s is not None)
    
    def test_added_legit_billing_profile(self, config : Config):
        s : str = config.configs["billing_account"]
        j : list[dict] = GetAzure.billing_profiles_associated_with_account(s)
        ids : list[str] = [d["id"] for d in j]
        id : str = config.configs["billing_profile"]
        assert id in ids


def test_costmanagement_exists():
    r = costmanagement_check.run_commandfile()
    print(r)
    assert r != ""

def test_storage_container_exists():
    l : list = Command.get_storagecontainers_with_account()
    print(l)
    assert len(l) > 0