import pytest
from src.cloud_levelup.command_files import GetAzure, Config
from src.cloud_levelup.parameters import databricks_config_filepath

def test_databricks_extension():
    result : str = GetAzure._result("az", "databricks", "-h")
    print(result)
    assert result != ""

def test_databricks_cli():
    result : str = GetAzure._result("databricks", "clusters", "-h")
    print(result)
    assert result != ""

def test_databricks_workspace_exists():
    j : list[dict] = GetAzure._json("az", "databricks", "workspace", "list", "--output", "json")
    print(j)
    assert(len(j) > 0)

def test_databricks_cluster_exists():
    j : list[dict] = GetAzure._json("databricks", "clusters", "list", "--output", "json")
    print(j)
    assert(len(j)>0)

def test_databricks_cluster_id_in_proper_place():
    configs : Config = Config(databricks_config_filepath)
    cluster_id : str = configs.configs["cluster1_id"]
    j : list[dict] = GetAzure._json("databricks", "clusters", "list", "--output", "json")
    print(j)
    assert(cluster_id in [d["cluster_id"] for d in j])

class TestClusterIsNotExpensive:

    @pytest.fixture(scope="class")
    def cluster_attrs(self) -> dict:
        configs : Config = Config(databricks_config_filepath)
        cluster_id : str = configs.configs["cluster1_id"]
        j : list[dict] = GetAzure._json("databricks", "clusters", "list", "--output", "json")
        cluster_attrs : dict = [d for d in j if d["cluster_id"] == cluster_id][0]
        return cluster_attrs
    
    def test_cluster_has_autotermination_30min_or_under(self, cluster_attrs : dict):
        print(cluster_attrs)
        assert(int(cluster_attrs["autotermination_minutes"]) <= 30)

    def test_cluster_is_single_node(self, cluster_attrs : dict):
        print(cluster_attrs)
        assert(cluster_attrs["is_single_node"])

    def test_cluster_is_d2_or_b_series(self, cluster_attrs : dict):
        print(cluster_attrs)
        assert("_d2" in str(cluster_attrs["node_type_id"]).lower() or "_b" in str(cluster_attrs["node_type_id"]).lower())

    def test_cluster_is_terminated(self, cluster_attrs : dict):
        print(cluster_attrs)
        assert(cluster_attrs["state"] == "TERMINATED")

def test_databricks_workspace_path_understand():
    configs : Config = Config(databricks_config_filepath)
    workspace_path : str = configs.configs["workspace_path"]
    j : list[dict] = GetAzure._json("databricks", "workspace", "list", workspace_path, "--output", "json")
    print(j)
    assert(len(j)>0)

def test_databricks_filesystem_contains_csv_file():
    configs = Config(databricks_config_filepath)
    dbfs_folderpath : str = configs.configs["dbfs_folderpath"]
    if dbfs_folderpath is None:
        pytest.fail(f"you need to enter a DBFS file path into the {databricks_config_filepath} with a csv file inside it.")
    j : list[dict] = GetAzure._json("databricks", "fs", "ls", dbfs_folderpath, "--output", "json")
    print(j)
    if not any([".csv" in d["name"] for d in j]):
        pytest.fail(f"you need to enter a DBFS file path into the {databricks_config_filepath} with a csv file inside it.")