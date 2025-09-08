# Welcome to Cloud Levelup!

This is a training ground for you to learn how to use Azure services. By completing this game you will be able to:

- Manage an Azure account
- Better understand Azure billing
- Use the azure-cli

## Level 0: LevelUp Cloud Setup

In this level, you will download this program and check that you have an azure account. cd into the package file, then do the following: 

```
.\winvenv\Scripts\activate <OR> source ./iosvenv/bin/activate
pytest tests\0_config_tests.py
```

All tests should pass. If they don't, check that you are in a virtual environment and consider running a troubleshooting script in the appropriate scripting language.

## Level 1: Azure Subscription, Resource Group, and Some Storage

In this level, you will need to login to Azure and do the following.
- create a subscription
- create a resource group
- create a storage account
- download the azure-cli on your working computer
- practice the following commands, which should return non-error states:
```
az <login|logout>
az ad signed-in-user show
az account list
az group <create|list>
az storage account list
```
Don't worry about using the cli to create a resource group or a storage account. Use the webportal for that. Use the cli for now to probe things in your account. After you explore these commands and get successful output, make sure that you have all required components by running `pytest tests\1_setup_tests.py`. These should all pass after you have your subscription used up. You will need to set up a resource group and a storage account, the latter associated with the former.
- Nothing in this level should cost money.
- Observe which features are associated with which attribute/object.

#### Troubleshooting

- make sure that you can run bash scripts or batch files for ios or windows, respectively. If you cannot due to permissions, you may run `bash ./troubleshooting/bash_file_permissions.sh` to ensure that all the `.sh` files are executable. To run bash scripts, make sure that they work with `bash <relative path to script>`.

## Level 2: Billing Accounts and Billing Profiles

NOTE: This level will ask you to explore billing information. Do NOT upload this section to another computer or give to anyone else. Run `pytest tests\2_billing_tests.py -vv` to test for this level.

This is a straightforward level that will check whether you understand how to find various __things__ (there's really no better word for it) in your Azure account. Note: if you're not working in your own personal account, you may or may not have access to these things. To pass tests in this level, do the following:
- Run `python do.py refresh_configs`. Run `python do.py --help` for info on the minimal cli of this program. This will import items into your my_config folder for you to fill out. The first two tests should pass now.
- In the file `costman_export.json` within `my_configs`, you will add the information you need to create a billing report for a billing profile.
    - You will need to add your billing account name to the first config. This account is the one containing the profile that you would like financial information about. If you add anything at all, another test will pass. If you add a correct billing account name, yet another test will pass. (Hint: we check `az billing account list --output json` to check your billing account `name`). Btw, you should run that cli command to determine if there is anything you would like to add to your billing account.
        - a billing account is a collection of billing profiles, billing addresses, and contact information.
        - a billing profile manages a single subscription. So when you signed up, you created a billing profile and a billing account that hosts it. It __must__ be the one associated with the billing account you entered for this level. __AGAIN__, do not post this information anywhere. Do not upload this information to github.
    - Add your billing profile __id__ (not a name) that you want to contain the cost management export. It must be associated with the previously added billing account. You can find this information with the `az billing profile list --account-name <your account name>` command. You should also be able to look this up with the Azure webportal. Yet another slew of tests should pass after you do this correctly. Look at the data associated with billing profiles. See what is and isn't there.

This wraps up level 2! There are a few questions that I don't understand yet, but for the most part, you will have observed: one billing account per profile, one subscription per billing profile and visa versa, one subscription per resource group, one resource group per storage account, and storage containers associated with a storage account. There are tons of Azure training levels associated with these items. Take them.

## Level 3: More Storage and Understanding Costs

NOTE: you will start to incur costs with this level! If you do not have a free account and do not want to pay anything then you should not go on to this level or subsequent levels. We will work to keep your costs low, but you should probably set up cost alerts.

For this level, you will be adding storage in your Azure webportal, and then adding them to your configs to ensure that you understand what goes where. The end result is a cost management export into a storage container that your created, as well as the ability to create new cost management exports via the CLI. Use `pytest tests/3_storage_tests.py -vv` for this level.

#### Install the costmanagement extension for the Azure cli.

- You will need to install the costmanagement extension for your cli. Now your first test should pass.

#### Create a Storage Container and Add Configs

- add your storage account id to the config file costman_export.json.
- by now you should understand how the configs work. Use the Azure webportal to create a storage container and put its name in the costman_export.json. This will cost a little bit of money each month.

#### Create a Cost Management Export (a report piping to a storage container)

- Go to the cost management page in your Azure web portal. Create an export, and assign it to the storage container that your just created. Make sure to finalize the creation of the cost management export. After you do this, yet another test should pass.
    - Note - now you also have a cost management export that you can run! This will help you manage your resources to ensure that you are not spending too much money.
- Fill out the remaining information, and make sure to name the report something other than the name of the first cost management export you created. Now you should be able to run `python do.py create_costman_export` and have it work! This script, whose template is in the `script_templates` folder, pulls from your configs to create a cost management export into a storage container via the CLI.
- You created a cost management export associated with a __billing profile__. How would you create a cost management export associated with a resource group?