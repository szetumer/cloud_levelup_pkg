import pytest
from src.cloud_levelup.command_files import GetAzure, Config
from src.cloud_levelup.parameters import billingexport_config_filepath

class TestCostManagementExport:

    @pytest.fixture(scope="class")
    def config(self) -> Config:
        c : Config = Config(billingexport_config_filepath)
        return c
        
    def test_create_a_cost_management_export(self, config : Config):
        j : list[dict] = GetAzure.storage_accounts()
        ids : list[str] = [d["id"] for d in j]
        config_id : str = config.configs["storage_account_id"]
        assert(config_id in ids)
    
    