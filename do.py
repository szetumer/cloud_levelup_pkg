from __future__ import annotations
import click
from pathlib import Path
from src.cloud_levelup.parameters import create_costman_export_configpath, create_costman_export_str, my_config_folderpath
import os

clearing_command_dict : dict[str, str] = {
    "costman_export.json"   : create_costman_export_str
}


def refresh_costman_export_configfile(p : Path, s : str) -> None:
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
def clear_config(filename : str):
    '''Clear the config file whose name you give'''
    filename : str = filename if ".json" in filename else filename + ".json"
    p : Path = my_config_folderpath / filename
    assert(p.exists())
    fill_with : str = clearing_command_dict.get(filename, "couldn't find file text")
    refresh_costman_export_configfile(p, fill_with)


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
    refresh_costman_export_configfile(create_costman_export_configpath, create_costman_export_str)


if __name__ == "__main__":
    cli()