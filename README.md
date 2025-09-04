# Welcome to Cloud Levelup!
This is a training ground for you to learn how to use Azure services.
- The goal of this project is to train you to develop in an Azure environment. Your goal is to be able to successfully run and pass tests within some sort of testing framework.

## level0: Getting Your Testing Enviroment Set Up
In this level, you will download this program and check that you have an azure account. cd into the package file, then do the following: 

```
.\venv\Scripts\activate <OR> source ./venv/bin/activate
pytest tests\config_tests.py
```

All tests should pass. Simple.

## level1: Getting an Azure Subscription
In this level, you will need to figure out how to configure your azure environment and set it up so that it can work for you. This will require an azure account. Get comfortable with these commands:
```
az login
az logout
az ad signed-in-user show
az account list
```