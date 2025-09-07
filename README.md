# Welcome to Cloud Levelup!
This is a training ground for you to learn how to use Azure services. By completing this game you will be able to:

- Manage an Azure account
- Use the azure-cli
- Better understand other tools such as batch and bash files

## Level 0: Getting Your Testing Enviroment Set Up
In this level, you will download this program and check that you have an azure account. cd into the package file, then do the following: 

```
.\winvenv\Scripts\activate <OR> source ./iosvenv/bin/activate
pytest tests\config_tests.py
```

All tests should pass. Simple. If you need to debug.

## Level 1: Setting Up an Azure Subscription, Resource Group, and Some Storage
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

## Level 2: Understanding Billing Accounts and Billing Profiles

This is a straightforward level that will check whether you understand how to find various __things__ (there's really no better word for it) in your Azure account. Note: if you're not working in your own personal account, you may or may not have access to these things. I'm not sure. Do the following:
- Run `python do.py refresh_configs`. Run `python do.py --help` for info on the minimal cli of this program. This will import items into your my_config folder for you to fill out.
- In the file costman_export.json, you will add the information you need to create a cost report for a billing profile.
    - Your first test of this level should pass.


## Level 3: More Storage and Understanding Costs

NOTE: you will start to incur costs with this level! If you do not have a free account and do not want to pay anything then you should not go on to this level or subsequent levels. We will work to keep your costs low, but explore budgeting and cost alerts. Use `pytest <tests> -rA` option to look at your answers.

SECOND NOTE: cli commands are getting longer and longer. For that reason, you will store configs for these CLI commands in the my_configs folder within this game. To create the empty configs for you to fill out,  Do the following, via your Azure portal:

#### Create a Storage Container

- Create a storage container, after which the first test will pass. (Note, it will fail if you have multiple storage accounts and the first one doesn't have a storage container).

#### Create a Cost Management Export (a report piping to a storage container)
- Familiarize yourself with additional commands `az billing account list` and `az billing profile list`. You need to understand the relationship between subscriptions, billing accounts, and billing profiles. These, resource groups and management groups, will determine the scope of the cost reports.
- You will need to install the costmanagement extension for your cli. Now your second test should pass.
- run the file `costreport` in the `query` folder.