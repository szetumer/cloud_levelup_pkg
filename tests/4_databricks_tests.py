import pytest
from src.cloud_levelup.command_files import GetAzure, Config
from src.cloud_levelup.parameters import databricks_config_filepath

def test_databricks_extension():
    result : str = GetAzure._result("az", "databricks", "-h")
    assert result != ""

def test_databricks_cli():
    result : str = GetAzure._result("databricks", "clusters", "-h")
    assert result != ""

def test_databricks_workspace_exists():
    j : list[dict] = GetAzure._json("az", "databricks", "workspace", "list", "--output", "json")
    assert(len(j) > 0)

def test_databricks_cluster_exists():
    j : list[dict] = GetAzure._json("databricks", "clusters", "list", "--output", "json")
    assert(len(j)>0)

def test_databricks_cluster_id_in_proper_place():
    configs : Config = Config(databricks_config_filepath)
    cluster_id : str = configs.configs["cluster1_id"]
    j : list[dict] = GetAzure._json("databricks", "clusters", "list", "--output", "json")
    assert(cluster_id in [d["cluster_id"] for d in j])
    
def test_databricks_workspace_path_understand():
    configs : Config = Config(databricks_config_filepath)
    workspace_path : str = configs.configs["workspace_path"]
    j : list[dict] = GetAzure._json("databricks", "workspace", "list", workspace_path, "--output", "json")
    assert(len(j)>0)

def test_account_has_keyvault():
    j : list[dict] = GetAzure._json("az", "keyvault", "list")
    assert(len(j)>0)

def test_databricks_has_secret_scope():
    j : list[dict] = GetAzure._json("databricks", "secrets", "list-scopes", "--output", "json")
    assert(len(j)>0)