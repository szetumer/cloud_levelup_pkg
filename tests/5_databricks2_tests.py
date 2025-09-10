import pytest
from src.cloud_levelup.parameters import databricks_config_filepath
from src.cloud_levelup.command_files import GetAzure, Config

@pytest.fixture(scope="session")
def db_configs() -> dict:
    return Config(databricks_config_filepath).configs

@pytest.fixture(scope="session")
def service_principal_info(db_configs) -> dict | None:
    db_app_name : str = db_configs["databricks_application_display_name"]
    j : list[dict] = GetAzure._json("az", "ad", "sp", "list", "--display-name", db_app_name, "--output", "json")
    if len(j) == 0:
        return None
    return j[0]

@pytest.fixture(scope="session")
def storage_account_info(db_configs) -> dict | None:
    storage_account_name : str = db_configs["storage_account_tomount_name"]
    j : list[dict] = GetAzure._json("az", "storage", "account", "list", "--output", "json")
    result : list[dict] = [d for d in j if d["name"] == storage_account_name]
    if len(result) == 0:
        return None
    return result[0]

@pytest.fixture(scope="session")
def keyvault_info(db_configs : dict) -> dict | None:
    j : list[dict] = GetAzure._json("az", "keyvault", "list", "--output", "json")
    keyvault_with_id : list[dict] = [d for d in j if d["id"] == db_configs["keyvault_id"]]
    if len(j) == 0:
        return None
    return keyvault_with_id[0]

class TestServicePrincipalSetup:
    def test_has_service_principal(self, service_principal_info):
        if service_principal_info is None:
            pytest.fail("you need to create a service principal in the app registration portal for your databricks.")
        assert(True)
    
    def test_storage_acc_added_to_configs(self, storage_account_info):
        if storage_account_info is None:
            pytest.fail("you need to add your storage account info to the config file")
        assert(True)
    
    def test_service_principal_has_storage_account_blob_access(self, service_principal_info, storage_account_info):
        j : list[dict] = GetAzure._json("az", "role", "assignment", "list", "--scope", storage_account_info["id"])
        sp_id_slash_name : str = service_principal_info["appId"]
        result : list[dict] = [d for d in j if
                               d["principalName"] == sp_id_slash_name and d["roleDefinitionName"] == "Storage Blob Data Contributor"]
        print(j)
        print(service_principal_info)
        assert(len(result) > 0)
    
    def test_service_principals_app_has_a_secret(self, service_principal_info):
        j : list[dict] = GetAzure._json("az", "ad", "app", "credential", "list", "--id", service_principal_info["appId"])
        print(j)
        assert(len(j)>0)

class TestKeyvaultSetup:
    def test_keyvault_id_added_correctly(self, keyvault_info : dict | None):
        if keyvault_info is None:
            pytest.fail(f"put the id of the keyvault into the config file {databricks_config_filepath}")
        assert(True)
    
    def test_keyvault_has_at_least_one_keyvault_secrets_user_added(self, keyvault_info : dict | None):
        assert(keyvault_info is not None)
        j : list[dict] = GetAzure._json("az", "role", "assignment", "list", "--scope", keyvault_info["id"])
        result : list[dict] = [d for d in j if d["roleDefinitionName"] == "Key Vault Secrets User"]
        assert(len(result) > 0)

def test_application_serviceprincipal_added_to_keyvault_role(service_principal_info : dict, keyvault_info : dict):
    if keyvault_info is None or service_principal_info is None:
        pytest.fail("get earlier tests to pass first")
        j : list[dict] = GetAzure._json("az", "role", "assignment", "list", "--scope", keyvault_info["id"], "--output", "json")
        print(j)
        j_result = [d for d in j if
                    d["principalType"] == "ServicePrincipal"
                    and d["principalName"] == service_principal_info["appId"]]
        assert(len(j_result)>0)
    

#These are premium tier tests. You don't need these points.
def test_application_has_been_registered(service_principal_info : dict):
    if service_principal_info is None:
        pytest.fail(f"register a databricks application and put the display name of an application in the {databricks_config_filepath} file under the appropriate part.")
    print(service_principal_info)
    assert(True)

def test_databricks_has_secret_scope():
    j : list[dict] = GetAzure._json("databricks", "secrets", "list-scopes", "--output", "json")
    assert(len(j)>0)

def test_databricks_secret_scope_has_type_of_azure_keyvault():
    j : list[dict] = GetAzure._json("databricks", "secrets", "list-scopes", "--output", "json")
    print(j)
    assert(len([d for d in j if d["backend_type"] == "AZURE_KEYVAULT"]))