import json
import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from src.cloud_levelup.parameters import get_system, commandspath

@dataclass
class CommandFile:
    win_filename : str
    ios_filename : str
    command_folderpath : ClassVar[Path] = commandspath

    @property
    def win_abspath(self) -> Path:
        return CommandFile.command_folderpath / self.win_filename

    @property
    def ios_abspath(self) -> Path:
        return CommandFile.command_folderpath / self.ios_filename

    def run_commandfile(self, *args) -> str:
        match get_system():
            case "Windows":
                return self.run(*[self.win_abspath, *args])
            case "iOs":
                return self.run(*[self.ios_abspath, *args])
            case "Linux":
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
            case _:
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")

    def get_commandfile_json(self, *args) -> list:
        result : str = self.run_commandfile(*args)
        return json.loads(result)
    
    @staticmethod
    def get_storageaccount_name(ith_account : int = 0) -> str:
        l : list = storageaccounts_command.get_commandfile_json()
        assert(len(l) > ith_account)
        storage_account : dict = l[ith_account]
        return storage_account["name"]
    
    @classmethod
    def get_storagecontainers_with_account(cls, accountname : str | None = None) -> list[dict]:
        if accountname is None: #just use the first account name
            accountname = cls.get_storageaccount_name()
        l : list = storagecontainers_command.get_commandfile_json(accountname)
        return l

    @staticmethod
    def run(*args : list[str|Path]) -> str:
        for o in args:
            assert(isinstance(o, str) or isinstance(o, Path))
        arglist = [o if isinstance(o, str) else str(o) for o in args]
        match get_system():
            case "Windows":
                arglist = arglist
            case "iOs":
                arglist = ["bash", *arglist]
            case "Linux":
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
            case _:
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
        result = subprocess.run(arglist, stdout=subprocess.PIPE, text=True)
        val : str = result.stdout[:-1] if result.stdout.__len__() > 0 and result.stdout[-1] == '\n' else result.stdout
        return val
    
    @classmethod
    def get_json(cls, *args : list[str|Path]) -> list:
        return json.loads(cls.run(*args))

@dataclass
class Command:
    @staticmethod
    def create_


config_command = CommandFile("config.bat", "config.sh")
azurecheck_command = CommandFile("check_azure.bat", "check_azure.sh")
subscriptions_command = CommandFile("get_subscriptions.bat", "get_subscriptions.sh")
resourcegroups_command = CommandFile("get_resgroups.bat", "get_resgroups.sh")
storageaccounts_command = CommandFile("get_storageaccounts.bat", "get_storageaccounts.sh")
storagecontainers_command = CommandFile("get_containers.bat", "get_containers.sh")
costmanagement_check = CommandFile("check_costmanagement.bat", "check_costmanagement.sh")