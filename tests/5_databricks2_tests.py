import pytest
from src.cloud_levelup.command_files import GetAzure

def test_account_has_keyvault():
    j : list[dict] = GetAzure._json("az", "keyvault", "list")
    assert(len(j)>0)

def test_databricks_has_secret_scope():
    j : list[dict] = GetAzure._json("databricks", "secrets", "list-scopes", "--output", "json")
    assert(len(j)>0)