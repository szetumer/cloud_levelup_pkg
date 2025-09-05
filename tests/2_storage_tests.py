import pytest
from src.cloud_levelup.command_files import CommandFile, costmanagement_check

def test_storage_container_exists():
    l : list = CommandFile.get_storagecontainers_with_account()
    print(l)
    assert len(l) > 0

def test_costmanagement_exists():
    r = costmanagement_check.run_commandfile()
    print(r)
    assert r != ""