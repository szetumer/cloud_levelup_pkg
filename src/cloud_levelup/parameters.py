from pathlib import Path
import platform
from typing import LiteralString, Literal
import os

ROOT_PATH = os.getcwd()
rootpath = Path(ROOT_PATH)
testspath = rootpath / "tests"
commandspath = rootpath / "commands"
my_config_folderpath = rootpath / "my_configs"
create_costman_export_configpath = rootpath / "my_configs" / "costman_export.json"
billingexport_config_filepath = rootpath / "my_configs" / "costman_export.json"
databricks_config_filepath = my_config_folderpath / "databricks_config.json"
rgraph_config_filepath = my_config_folderpath / "rgraph_queries.json"
scripttemplate_folderpath = rootpath / "script_templates"
level_moreaccounting_folderpath = rootpath / "level6_more_accounting"

def get_system() -> Literal["Windows"] | Literal["iOs"] | Literal["Linux"]:
    if platform.system() == "Windows":
        return "Windows"
    elif platform.system() == "Linux":
        return "Linux"
    elif os.name == "posix":
        return "iOs"
    else:
        raise NotImplementedError(f"cannot recognize system of {platform.system()} and/or {os.name}")


create_costman_export_str : str = '''
{
    "billing_account" : null,
    "billing_profile" : null,
    "reportname" : null,
    "storage_account_id" : null,
    "storage_container_name" : null,
    "storage_directory" : "CostReports"
}'''

databricks_config_str : str = '''
{
    "cluster1_id"       : null,
    "workspace_path"    : null,
    "dbfs_folderpath"   : null,
    "keyvault_id"       : null,
    "databricks_application_display_name" : null,
    "storage_account_tomount_name" : null,
    "db_application_scopename" : null
}'''

rgraph_config_str : str = '''
{
    "tests_to_run"      : [0, 1],
    "query1"            : null,
    "query3"            : null
}'''