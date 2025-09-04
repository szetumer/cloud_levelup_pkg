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

    def run(self, *args) -> str:
        match get_system():
            case "Windows":
                return self._run(self.win_abspath, *args)
            case "iOs":
                return self._run(self.ios_abspath, *args)
            case "Linux":
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")
            case _:
                raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")

    @staticmethod
    def _run(filepath : Path, *args) -> str:
        filepath_string = str(filepath)
        arglist = [filepath_string] if not args else [filepath_string, *args]
        result = subprocess.run(arglist, stdout=subprocess.PIPE, text=True)
        val : str = result.stdout[:-1] if result.stdout.__len__() > 0 and result.stdout[-1] == '\n' else result.stdout
        return val


config_command = CommandFile("config.bat", "config.sh")
azurecheck_command = CommandFile("check_azure.bat", "check_azure.sh")
get_subscriptions_command = CommandFile("get_subscriptions.bat", "get_subscriptions.sh")