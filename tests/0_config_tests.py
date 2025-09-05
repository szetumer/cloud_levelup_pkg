import pytest
from pathlib import Path
from src.cloud_levelup.parameters import rootpath, testspath, commandspath, get_system
from src.cloud_levelup.command_files import (CommandFile, config_command, azurecheck_command,
                                             subscriptions_command, resourcegroups_command, storageaccounts_command)

@pytest.mark.parametrize(
        "o", [
          (rootpath)
        , (testspath)
        , (commandspath)
        , (config_command)
        , (subscriptions_command)
        , (azurecheck_command)
        , (resourcegroups_command)
        , (storageaccounts_command)
        ]
)
def test_files_exist(o : Path | CommandFile):
        if isinstance(o, Path):
                assert o.exists()
        elif isinstance(o, CommandFile):
                assert o.win_abspath.exists()
                assert o.ios_abspath.exists()


@pytest.mark.skipif(get_system() != "Windows", reason = "skipping Windows tests")
class TestWindows:
        def test_is_windows(self):
                assert get_system() == "Windows"
        
        def test_config_filerun(self):
               assert config_command.run() == "Hello, World!"

        def test_have_azure_cli(self):
               assert azurecheck_command.run() != ""

@pytest.mark.skipif(get_system() != "iOs", reason = "skipping iOs tests")
class TestIos:
        def test_is_iOs(self):
                assert get_system() == "iOs"
        
        def test_config_filerun(self):
                assert config_command.run() == "Hello, World!"

        def test_have_azure_cli(self):
               assert azurecheck_command.run() != ""

def test_imports_are_present():
       import azure.cli
       import pytest
       assert True