from __future__ import annotations
import json
import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from src.cloud_levelup.parameters import get_system, commandspath, my_config_folderpath
from src.cloud_levelup.parameters import scripttemplate_folderpath


@dataclass
class Command:
    win_filename : str
    ios_filename : str
    command_folderpath : ClassVar[Path] = commandspath

    @property
    def win_abspath(self) -> Path:
        return Command.command_folderpath / self.win_filename

    @property
    def ios_abspath(self) -> Path:
        return Command.command_folderpath / self.ios_filename

    def run_commandfile(self, *args) -> str:
        match get_system():
            case "Windows":
                return self.run(True, *[self.win_abspath, *args])
            case "iOs":
                return self.run(True, *[self.ios_abspath, *args])
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
    def run(add_bash : bool = True, *args) -> str:
        for o in args:
            assert(isinstance(o, str) or isinstance(o, Path))
        arglist = [o if isinstance(o, str) else str(o) for o in args]
        match get_system():
            case "Windows":
                arglist = arglist
            case "iOs":
                arglist = ["bash", *arglist] if add_bash else arglist
            case "Linux":
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
            case _:
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
        for item in arglist:
            print(item)
        result = subprocess.run(arglist, stdout=subprocess.PIPE, text=True)
        val : str = result.stdout[:-1] if result.stdout.__len__() > 0 and result.stdout[-1] == '\n' else result.stdout
        return val
    
    @classmethod
    def run_create_costmanagement_export_from_configfile(cls) -> str:
        config = Config(my_config_folderpath / "costman_export.json")
        filename : str = "create_costman_export.bat" if get_system() == "Windows" else "create_costman_export.sh"
        result = cls.run(True, str(scripttemplate_folderpath / filename),
                         config.configs["billing_profile"],
                         config.configs["reportname"],
                         config.configs["storage_account_id"],
                         config.configs["storage_container_name"],
                         config.configs["storage_directory"]
                         )
        return result
    
    @classmethod
    def run_costman_query_from_configfile(cls) -> str:
        config = Config(my_config_folderpath / "costman_export.json")
        filename : str = "costman_query.bat" if get_system() == "Windows" else "costman_query.sh"
        result = cls.run(True, str(scripttemplate_folderpath / filename),
                         config.configs["billing_profile"]
        )
        return result

    @classmethod
    def get_json(cls, add_bash : bool, *args : list[str|Path]) -> list:
        return json.loads(cls.run(add_bash, *args))

@dataclass
class Config:
    def __init__(self, filepath : Path) -> None:
        with open(filepath, "r+") as f:
            s : str = f.read()
            self.configs : dict[str, str] = json.loads(s)
            f.close()

class GetAzure:

    @staticmethod
    def _result(*arglist) -> str:
        match get_system():
            case "Windows":
                result = subprocess.run(arglist, stdout=subprocess.PIPE, shell=True, text=True)
            case "iOs":
                result = subprocess.run(arglist, stdout=subprocess.PIPE, text=True)
            case _:
                raise NotImplementedError(f"have not implemented system for {get_system()}")
        val : str = result.stdout[:-1] if result.stdout.__len__() > 0 and result.stdout[-1] == '\n' else result.stdout
        return val
    
    @classmethod
    def _json(cls, *arglist) -> list[dict]:
        str_result : str = cls._result(*arglist)
        return json.loads(str_result)

    @classmethod
    def billing_account_names(cls) -> list[str]:
        j : list[dict] = cls._json("az", "billing", "account", "list", "--output", "json")
        return [d["name"] for d in j]
    
    @classmethod
    def billing_profiles_associated_with_billingaccount_names(cls, s : str):
        j : list[dict] = cls._json("az", "billing", "profile", "list", "--account-name", s, "--output", "json")
        return j
    
    @classmethod
    def storage_accounts(cls) -> list[dict]:
        j : list[dict] = cls._json("az", "storage", "account", "list", "--output", "json")
        return j
    
    @classmethod
    def storage_containers_associated_with_storageaccount_name(cls, storage_account_name : str) -> list[dict]:
        j : list[dict] = cls._json("az", "storage", "container", "list", "--account-name", storage_account_name, "--auth-mode", "login", "--output", "json")
        return j
    
    @classmethod
    def costmanagement_exports_associated_with_billingprofile_id(cls, billing_profile_id : str):
        j : list[dict] = cls._json("az", "costmanagement", "export", "list", "--scope", billing_profile_id, "--output", "json")
        return j
    
    @classmethod
    def storage_account_names_associated_with_id(cls, storage_account_id : str) -> list[str]:
        j : list[dict] = cls.storage_accounts()
        names : list[str] = [d["name"] for d in j if d["id"] == storage_account_id]
        assert(len(names) > 0)
        return names
        

config_command = Command("config.bat", "config.sh")
azurecheck_command = Command("check_azure.bat", "check_azure.sh")
subscriptions_command = Command("get_subscriptions.bat", "get_subscriptions.sh")
resourcegroups_command = Command("get_resgroups.bat", "get_resgroups.sh")
storageaccounts_command = Command("get_storageaccounts.bat", "get_storageaccounts.sh")
storagecontainers_command = Command("get_containers.bat", "get_containers.sh")
costmanagement_check = Command("check_costmanagement.bat", "check_costmanagement.sh")