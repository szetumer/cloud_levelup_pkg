from __future__ import annotations
import click
from pathlib import Path
from src.cloud_levelup.parameters import (create_costman_export_configpath, create_costman_export_str, my_config_folderpath,
                                          databricks_config_filepath, databricks_config_str)
from src.cloud_levelup.command_files import Config, GetAzure, Command
import os

refresh_config_registry : dict[str, str] = {
    "costman_export.json"   : create_costman_export_str,
    "databricks_config.json": databricks_config_str
}

def _refresh_configfile(p : Path, s : str) -> None:
    with open(p, "w+") as f:
        f.write(s)
        f.close()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Please provide command. For help use --help")
    else:
        click.echo(f"Running: {ctx.invoked_subcommand}")

@cli.command()
@click.argument('filename')
def refresh_config(filename : str):
    '''Clear the config file whose name you give'''
    filename_s : str = filename if ".json" in filename else filename + ".json"
    assert(filename_s in refresh_config_registry.keys())
    p : Path = my_config_folderpath / filename_s
    fill_with : str = refresh_config_registry.get(filename_s, "couldn't find file text")
    _refresh_configfile(p, fill_with)

@cli.command()
def create_costman_export():
    p : Path = my_config_folderpath / "costman_export.json"
    assert(p.exists())
    config : Config = Config(p)
    for k, v in config.configs.items():
        assert(v is not None)
    billingaccount_names : list = GetAzure.billing_account_names()
    assert config.configs["billing_account"] in billingaccount_names
    billingprofiles : list =  GetAzure.billing_profiles_associated_with_billingaccount_names(config.configs["billing_account"])
    assert config.configs["billing_profile"] in [d["id"] for d in billingprofiles]
    storageaccounts : list[dict] = GetAzure.storage_accounts()
    assert config.configs["storage_account_id"] in [d["id"] for d in storageaccounts]
    storageaccount_names = GetAzure.storage_account_names_associated_with_id(config.configs["storage_account_id"])
    assert(len(storageaccount_names) > 0)
    j : list[dict] = GetAzure.storage_containers_associated_with_storageaccount_name(storageaccount_names[0])
    assert config.configs["storage_container_name"] in [d["name"] for d in j]
    result : str = Command.run_create_costmanagement_export_from_configfile()
    print(result)

@cli.command()
def refresh_configs():
    '''Clear all config files'''
    config_folder : Path = Path(os.getcwd()) / "my_configs"
    if len(list(config_folder.iterdir())) > 1:
        print("To refresh your configs, please delete all files in my_config folder.\nThose are your configs to set up. You still need to delete the following files:")
        for p in config_folder.iterdir():
            if ".gitignore" not in str(p):
                print(p)
        return
    _refresh_configfile(create_costman_export_configpath, create_costman_export_str)
    _refresh_configfile(databricks_config_filepath, databricks_config_str)

if __name__ == "__main__":
    cli()