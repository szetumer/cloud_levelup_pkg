# Welcome to Cloud Levelup!

This is a training ground for you to learn how to use Azure services. By completing Cloud Levelup you will be able to:

- setup an Azure account
- better understand Azure billing
- manage Azure storage
- use the azure cli
- use the databricks cli
- run a databricks workflow
- mount Azure storage into the databricks file system

Please complete levels 0 through 3 before moving on to your favorite application. Completing Cloud Levelup __will__ cost money, so it is essential that you are comfortable learning the boring stuff (billing) before doing __anything else__ with Azure.

## Level 0: Cloud Levelup Setup

In this level, you will clone this github repo and check that things are set up appropriately. After cloning this github repo, cd into the package directory and start your virtual environment like so: 

```
.\winvenv\Scripts\activate <OR> source ./iosvenv/bin/activate
pytest tests\0_config_tests.py
```

All tests should pass. If they don't, check that you are in a virtual environment and consider running a troubleshooting script in the appropriate scripting language. We have two virtual environments for ios and windows, which is overkill, but it reduces the dependencies for those who don't want to deal with docker.

#### Level 0 Summary

You completed level 0, and set up your learning environment. This is the similar setup for all Levelup repos. Throughout these levels, we will use various cli commands to give you points for correctly doing tasks. You will work through the level using `pytest tests/<levelnumber>_<levelname>_tests.py` to track your progress.

## Level 1: Azure Subscription, Resource Group, and Some Storage

To complete this level, do the following:
- create a subscription
- create a resource group
- create a storage account
- download the azure-cli on your learning computer

Get comfortable with these cli commands:
```
az <login|logout>
az ad signed-in-user show
az account list
az group <create|list>
az storage account list
```
Don't worry about using the cli to create a resource group or a storage account. Use the webportal for that. Use the cli for now to probe for the state of your account. After you explore these commands and get successful output, make sure that you have all required components by running `pytest tests\1_setup_tests.py`. These should all pass after you have your subscription used up. You will need to set up a resource group and a storage account, the latter associated with the former.
- Nothing in this level should cost money.
- If nothing works, make sure you are logged into the right account using the above cli commands.
- If the cli commands don't work, make sure the azure cli has been installed. Consider using the scripts in the troubleshooting folder.
- Observe which features are associated with which attribute/object within your Azure account by using the above cli commands.
- Make sure that you can run bash scripts or batch files for ios or windows, respectively. If you cannot due to permissions, you may run `bash ./troubleshooting/bash_file_permissions.sh` to ensure that all the `.sh` files are executable. To run bash scripts, make sure that they work with `bash <relative path to script>`.

#### Notes:

A storage account associates storage containers with a resource group and, therefore, a billing profile. It allows Microsoft to charge you for specific storage.

## Level 2: Billing Accounts and Billing Profiles

Whew! That was an annoying level. Setting things up is always a pain. This level will ask you to explore billing information. Do NOT upload the data from this section to another computer or give to anyone else. Run `pytest tests\2_billing_tests.py -vv` to test for this level. Note: if you're not working in your own personal account, you may or may not have access to these parts of an Azure account.

To pass tests in this level, and get all the points, do the following:

- (+2 Points) Run `python do.py refresh_configs`. This will import files into your `my_configs` folder for you to fill out. Run `python do.py --help` for info on the minimal cli of the Cloud Levelup game.

- In the file `costman_export.json` within `my_configs`, you will add the information you need to create a billing report for a billing profile.

    - (+2 Points) You will need to add your billing account name to the first config. This billing account is the one containing the profile that you would like financial information about. If you add anything at all, another test will pass. If you add a correct billing account name. (Hint: we check `az billing account list --output json` to check your billing account `name`).
        - a billing account is a collection of billing profiles, billing addresses, and contact information.
        - a billing profile manages a single subscription. So when you signed up, you created a billing profile and a billing account that hosts it. It __must__ be the one associated with the billing account you entered for this level. __AGAIN__, do not post this information anywhere. Do not upload this information to github.

    - (+? Points) Add your billing profile __id__ (not a name) that you want to track financially. It must be associated with the previously added billing account. You can find this information with the `az billing profile list --account-name <your account name>` command. You should also be able to look this up with the Azure webportal. Look at the data associated with billing profiles. See what is and isn't there.

#### Level 2 Summary

This wraps up level 2! You will have observed: one billing account per profile, one subscription per billing profile and visa versa, one subscription per resource group, one resource group per storage account, and storage containers associated with a storage account. There are tons of Azure training levels associated with these items. Take them.

## Level 3: More Storage and Understanding Costs

NOTE: you will start to incur costs with this level! If you do not have a free account and do not want to pay anything then you should not go on to this level or subsequent levels. We will work to keep your costs low, but you should probably set up cost alerts as well.

In level 3, you will add storage information to your Resource Group. The end result is a cost management export into a storage container that your created, as well as the ability to create new cost management exports via the Azure CLI. Use `pytest tests/3_storage_tests.py -vv` for this level.

#### Install the costmanagement extension for the Azure cli.

- You will need to install the costmanagement extension for your cli. Now your first test should pass.

#### Create a Storage Container and Add Configs

- add your storage account id to the config file costman_export.json. This will pass additional tests.

- Use the Azure webportal to create a storage container and put its name in the costman_export.json. This will cost a little bit of money each month. More tests will pass.

#### Create a Cost Management Export (a report piping to a storage container)

- Go to the cost management page in your Azure web portal. Create an export, and assign it to the storage container that your just created. Make sure to finalize the creation of the cost management export. After you do this, yet another test should pass.
    - Note - now you also have a cost management export that you can run! This will help you manage your resources to ensure that you are not spending too much money.

- Fill out the remaining information, and make sure to name the report something other than the name of the first cost management export you created. Now you should be able to run `python do.py create_costman_export` and the azure cli will create a second cost management report right from your terminal! This script, whose template is in the `script_templates` folder, pulls from your configs to create a cost management export into a storage container via the CLI. You can take the `create_costman_export.<extension>` for your own use.

- You created a cost management export associated with a __billing profile__. How would you create a cost management export associated with a resource group?

- Run these cost management exports via the Azure webportal. The results should be ready within a day.

#### Summary of Levels 2 and 3
In these levels, you learned a little bit about budgeting in Azure and a little bit about storage. You will learn a lot more, but from here on out, the levels don't need to be taken sequentially.

## Additional Levels

Open the readme file contained in a folder whose levels you would like to complete using your favorite code editor. Follow the instructions and use the `pytest tests/<level number>_<levelname>_tests.py [-rA -rX and/or -vv]` method to track your progress. Levels are as follows:

#### learning databricks - Levels 4, 5
#### cleaning up resources - Level 6