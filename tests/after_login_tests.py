import pytest
from src.cloud_levelup.command_files import subscriptions_command

'''
You need to make sure you are already logged on.
'''

def test_get_subscriptions():
    j : list = subscriptions_command.get_json()
    print(j)
    assert len(j) > 0