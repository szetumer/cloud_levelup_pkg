import pytest
from src.cloud_levelup.command_files import subscriptions_command, resourcegroups_command, storageaccounts_command

'''
You need to make sure you are already logged on.
'''

def test_get_subscriptions():
    j : list = subscriptions_command.get_json()
    assert len(j) > 0

def test_get_resource_groups():
    j : list = resourcegroups_command.get_json()
    assert len(j) > 0

def test_get_storage_accounts():
    j : list = storageaccounts_command.get_json()
    assert len(j) > 0