# Welcome to Cloud Levelup!
This is a training ground for you to learn how to use Azure services.
- The goal of this project is to train you to develop in an Azure environment. Your goal is to be able to successfully run and pass tests within some sort of testing framework.

## Level 0: Getting Your Testing Enviroment Set Up
In this level, you will download this program and check that you have an azure account. cd into the package file, then do the following: 

```
.\winvenv\Scripts\activate <OR> source ./iosvenv/bin/activate
pytest tests\config_tests.py
```

All tests should pass. Simple.

## Level 1: Setting Up an Azure Subscription, Resource Group, and Some Storage
In this level, you will
- create a subscription
- create a resource group
- create a storage account

You will need to figure out how to configure your azure environment and set it up so that it can work for you. Get comfortable with these commands:
```
az <login|logout>
az ad signed-in-user show
az account list
az group <create|list>
az storage account list
```
Don't worry about using the cli to create a resource group or a storage account. Use the webportal for that. After you explore these commands and get successful output, make sure that you have all required components by running `pytest tests\setup_tests.py`. These should all pass after you have your subscription used up. You will need to set up a resource group and a storage account, the latter associated with the former.
- Nothing in this level should cost money.
- Observe which features are associated with which attribute/object.

## Level 2: More Storage and Understanding Costs
NOTE: you will start to incur costs with this level! If you do not have a free account and do not want to pay anything then you should not go on to this level or subsequent levels. We will work to keep your costs low, but explore budgeting and cost alerts. Use `pytest <tests> -rA` option to look at your answers.

SECOND NOTE: cli commands are getting longer and longer. For that reason, you will store configs for these CLI commands in the my_configs folder within this folder. To create the empty configs for you to fill out, run `python do.py refresh_configs`. Run `python do.py --help` for info on the minimal cli.

#### Creating Storage Containers

- Create a storage container, after which the first test will pass. (Note, it will fail if you have multiple storage accounts and the first one doesn't have any).

#### Creating a Cost Management Export (a report piping to a storage container)
- Familiarize yourself with additional commands `az billing account list` and `az billing profile list`. You need to understand the relationship between subscriptions, billing accounts, and billing profiles. These, resource groups and management groups, will determine the scope of the cost reports.
- 
- You will need to install the costmanagement extension for your cli. Now your second test should pass.
- run the file `costreport` in the `query` folder.