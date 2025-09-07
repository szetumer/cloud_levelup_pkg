import pytest
from src.cloud_levelup.command_files import CommandFile

def test_get_storageaccount():
    assert "" == CommandFile.get_storageaccount_name()