from pathlib import Path
from src.cloud_levelup.parameters import create_costman_export_configpath
import os

create_costman_export_str : str = '''
{
    "billing_profile" : null,
    "reportname" : null,
    "storage_account_id" : null,
    "storage_container_name" : null,
    "storage_directory" : "CostReports"
}
'''

def refresh_costman_export_configfile() -> None:
    with open(create_costman_export_configpath, "w+") as f:
        f.write(create_costman_export_str)
        f.close()

def main() -> None:
    config_folder : Path = Path(os.getcwd()) / "my_configs"
    if len(list(config_folder.iterdir())) > 0:
        print("To refresh your configs, please delete all files in my_config folder.\nThose are your configs to set up. You still need to delete the following files:")
        for p in config_folder.iterdir():
            print(p)
        return
    refresh_costman_export_configfile()


if __name__ == "__main__":
    main()