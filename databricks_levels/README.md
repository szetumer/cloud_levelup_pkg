# Levelup Databricks

In these levels we will use the pytest testing framework to gradually learn how to use databricks. By now, you should have taken levels 0-3, and all the tests which are run by the command `pytest tests/#_levelname_tests.py` should pass. Similarly running the tests for levels 4 and 5, you should see many if not all tests failing. Your goal is to get all these tests to pass.

Let's levelup!

## Level 4: Databricks, Part 1

Levels 0 through 3 were a little rocky, I'm not going to lie. Now that you have the hang of how this works, let's move on to more valuable services that you can do with your azure account. Here are your tasks:

- (+1 Point) Install the Azure Databricks azure-cli extension.

- (+1 Point) Install __another__ cli, the databricks-cli (not an extension). (https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/tutorial?source=recommendations)

- (+1 Point : `az databricks workspace list --output json`) Create an Azure Databricks workspace via the webportal. Notice that each workspace requires a ResourceGroup.
    - What other unique __things__ are associated to a workspace? Eg, is workspace associated with a unique storage container? What about a unique billing profile?

- run `databricks configure`. Make sure your auth token is not stored in a public space. There is no test for this step.

- (+1 Point: `databricks clusters list --output json`) Create a cluster. This is a profile of a set of computers that will do work for you when you want them to. Running them costs money. Terminating their runs does not.

- (+1 Point) Use the cli to get the cluster id, and put that cluster id into the `databricks_config.json` file in the `my_configs` folder.

- (+3 or so Points : `databricks clusters list --output json`) When you create a cluster, the defaults will be fairly expensive, likely over $2 DBU/h. For learning, this can quickly rack up costs. To reduce costs, do the following:
    - set the autotermination_minutes to something under 30. A test will pass for this.
    - set the Node Type to single node, passing another test.
    - Choose a virtual machine from the D2 series, passing another test. If you can get something from the B series, apparently this is cheaper and your test should still pass, but it wasn't offered in my region.
    - I would recommend turning off photon acceleration. I couldn't figure out how to test for this.
    - Check the right hand corner of your compute configure screen, and you should see a price under $1 DBU/h. I got mine to ~ $0.50 DBU/h, but that was as low as I could muster. This is not tested.

###### TROUBLESHOOTING:
1) You must have a chargeable account to associate to a cluster. I experienced errors when my free subscription ran out.
2) Consider running `databricks configure`.
3) The system will not prevent you from configuring a cluster that will never startup due to resource requirements, eg min cores out of range.

- Activate your cluster via the Azure webportal. This could take as long as five minutes to activate. There is not test for this.

- (+1 Point) Use `databricks clusters delete <CLUSTER-ID>` to terminate (not actually delete) your cluster. If your cluster is terminated.

______

Take a moment to pat yourself on the back. Using these resources is not easy and you've taken a strong step towards minimizing costs of your Azure learning experience. You may use these tests in your projects however you like to minimize costs. They are marked under the test class `TestClusterIsNotExpensive` in the `4_databricks1_tests.py` file.
_____

#### More about workbooks

- (+1 Point :`databricks workspace list <Workspace Path>`) Add your workspace path to your `databricks_config.json` file and create a workbook within that workspace. Use the Azure databricks webportal to find the path of your workspace. Another test should pass. Note: this test uses the databricks cli whereas the first test of your ability to create databricks workspaces used the databricks extension of the azure cli. 

- Explore that cli command: what happens if you put the work-__book__ path into the cli command instead of the work-__space__ path? Does that say something about how workbooks are referenced internally?

- Take the following training to get some background on databricks:
    - https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/
    - https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/
    - https://learn.microsoft.com/en-us/training/modules/perform-data-analysis-azure-databricks/
    - https://learn.microsoft.com/en-us/training/paths/data-engineer-azure-databricks/

Personally, I found it very difficult to do any of the exercises with my own account, which is a shame. However, you can accomplish many of them with a small amount of sample data by downloading data from this website: https://raw.githubusercontent.com/MicrosoftLearning/mslearn-databricks/main/data/products.csv. You can't just import the data because it won't be in the DBFS. Instead, go to a workbook, then File>>Upload data to DBFS, and then select your csv. You'll get a path such as "dbfs:/FileStore/Workspace/<etc.>".

- Use this to check that you have correctly uploaded data within a cell of a workbook:
    
    ```
    spark.read.format("csv").option("header", "true").load("dbfs:/FileStore/<address given during upload>")
    ```

- (+1 Point :`databricks fs ls <filepath>`) Add the filepath (the thing that starts with "dbfs:/") to the `databricks_config.json` in the `dbfs_folderpath` config. If it contains a csv file, another test should pass.

#### Summary for Level 4

In this level you created a databricks cluster, workspace, and uploaded a file into the Databricks File System. You also learned how to probe for state via the azure cli and the databricks cli, which is great. You took some Microsoft training and you configured your databrick compute to reduce costs. Good job.

Bonus Content: because you installed the databricks extension and databricks cli, you can now shut down your clusters programmatically. One of your commands is `python do.py shutdown` which will terminate any clusters still active and log you out. The function itself can be found in the `azure_shutdown.py` and `command_files.py` files. Feel free to use them with proper citations.

## Level 5: Connecting Databricks to Storage Containers

Databricks are not intrinsically connected to datalakes or any other part of your Azure account. The process of connecting Azure storage to databricks is called "mounting". We will discuss how to mount storage containers into databricks.

- Learn about RBAC (Role Based Access Controls) and Service Principals. You can take Microsoft training for these subjects. There are no points associated with this activity though.

- Create a Service Principal, which is like a user/security profile for an application, within your Azure account. As of this writing, this is available through the Azure Entra ID portal >> Manage >> App registration. This creates an application object.

- To connect your azure storage blobs to a DBFS, you will now need to learn about secrets, secret scopes, keyvaults, keys, and RBAC (role based access control). This is a good link: [Understanding Secrets](https://mainri.ca/2024/10/06/dbutils-secrets-and-secret-scopes/#:~:text=To%20create%20and%20manage%20secret%20scopes%2C%20you%20can,Key%20Vault-backed%20secret%20scope%201%3A%20Go%20to%20https%3A%2F%2F%3Cdatabricks-instance%3E%2F%23secrets%2FcreateScope).
    - note: these are __not__ the same scopes that we used to create a financial report in level 2.

#### Creating an Azure Key Vault-backed secret scope

- `az keyvault list` In your azure webportal, go to the keyvault and create a keyvault. This is a place to store security keys. Another test should pass after you successfully create your keyvault.

- add yourself as a "Key Vault Administrator". Create a key in the keyvault.

- `databricks secrets list-scopes`. Go to https://<databricks-instance>/#secrets/createScope. Enter the name of the secret scope, address of the scope, etc. This step was fairly tricky so far. Yet another test should pass when you get a secret scope set up.