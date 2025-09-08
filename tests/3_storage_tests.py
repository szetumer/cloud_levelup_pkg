import pytest
from src.cloud_levelup.command_files import GetAzure, Config, costmanagement_check, Command
from src.cloud_levelup.parameters import billingexport_config_filepath


def test_costmanagement_extension_exists():
    r = costmanagement_check.run_commandfile()
    assert r != ""

def test_storage_container_exists():
    l : list = Command.get_storagecontainers_with_account()
    print(l)
    assert len(l) > 0

class TestCostManagementExport:

    @pytest.fixture(scope="class")
    def config(self) -> Config:
        c : Config = Config(billingexport_config_filepath)
        return c

    def test_config_has_info_on_storage_container(self, config : Config):
        storage_account_id : str = config.configs["storage_account_id"]
        storage_account_names : list[str] = GetAzure.storage_account_names_associated_with_id(storage_account_id)
        j : list[dict] = GetAzure.storage_containers_associated_with_storageaccount_name(storage_account_names[0])
        assert len(j) > 0
        container_names = [d["name"] for d in j]
        assert config.configs["storage_container_name"] in container_names
    
    def test_costmanagement_export_exists(self, config : Config):
        billing_profile_id : str = config.configs["billing_profile"]
        j : list[dict] = GetAzure.costmanagement_exports_associated_with_billingprofile_id(billing_profile_id)
        assert(len(j) > 0)