import pytest
from src.cloud_levelup.command_files import GetAzure

def test_databricks_extension():
    result : str = GetAzure._result("az", "databricks", "-h")
    assert result != ""

def test_databricks_workspace_exists():
    j : list[dict] = GetAzure._json("az", "databricks", "workspace", "list", "--output", "json")
    assert(len(j) > 0)