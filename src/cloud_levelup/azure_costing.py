import json
from pathlib import Path
from src.cloud_levelup.command_files import GetAzure
from src.cloud_levelup.parameters import level_moreaccounting_folderpath
'''
LEGEND
ga = GetAzure = thin wrapper around Azure CLI
dbws = databricks workspace
rg = resource graph
rgq = resource graph query
rgs = resource graph string
'''

ACCOUNTING_OUTPUT_FOLDERPATH : Path = level_moreaccounting_folderpath

def _ga_dbws(workspace_name : str, resource_group_name : str) -> dict:
    result : list[dict] = GetAzure._json("az", "databricks", "workspace", "show", "--name", workspace_name, "--resource-group", resource_group_name, "--output", "json")
    assert(isinstance(result, dict))
    return result

def _dbws_is_vnet_enabled(db_workspace_info : dict) -> bool:
    parameters : dict = db_workspace_info["parameters"]
    if parameters.get("enableNoPublicIp", {"value" : False})["value"] == True:
        return True
    return False

def _rgs_minimal():
    return "resources | where type =~ 'microsoft.databricks/workspaces' | count"

def _rgs_return5():
    return "resources | where type =~ 'microsoft.databricks/workspaces' | project name, type | limit 5"

def _rgs_query(rgs : str):
    result = GetAzure._json("az", "graph", "query", "-q", rgs, "--output", "json")
    return result

def _output_json_file(j_str : dict | list, filename : str, folderpath : Path = ACCOUNTING_OUTPUT_FOLDERPATH):
    p : Path = folderpath / filename
    with open(p, "w") as f:
        f.write(json.dumps(j_str, indent=3))
        f.close()
    return