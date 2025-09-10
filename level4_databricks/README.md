# Levelup Databricks

In these levels we will use the pytest testing framework to gradually learn how to use databricks. By now, you should have taken levels 0-3, and all the tests which are run by the command `pytest tests/#_levelname_tests.py` should pass. Similarly running the tests for levels 4 and 5, you should see many if not all tests failing. Your goal is to get all these tests to pass.

Let's levelup!

## Level 4: Databricks, Part 1

Levels 0 through 3 were a little rocky, I'm not going to lie. Now that you have the hang of how this works, let's move on to more valuable services that you can do with your azure account. Here are your tasks:

- __(+1 Point)__ Install the Azure Databricks azure-cli extension.

- __(+1 Point)__ Install __another__ cli, the databricks-cli (not an extension). (https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/tutorial?source=recommendations)

- __(+1 Point : `az databricks workspace list --output json`)__ Create an Azure Databricks workspace via the webportal. Notice that each workspace requires a ResourceGroup.
    - What other unique __things__ are associated to a workspace? Eg, is workspace associated with a unique storage container? What about a unique billing profile?

- run `databricks configure`. Make sure your auth token is not stored in a public space. There is no test for this step.

- __(+1 Point: `databricks clusters list --output json`)__ Create a cluster. This is a profile of a set of computers that will do work for you when you want them to. Running them costs money. Terminating their runs does not.

- __(+1 Point)__ Use the cli to get the cluster id, and put that cluster id into the `databricks_config.json` file in the `my_configs` folder.

- __(+3 or so Points : `databricks clusters list --output json`)__ When you create a cluster, the defaults will be fairly expensive, likely over $2 DBU/h. For learning, this can quickly rack up costs. To reduce costs, do the following:
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

- __(+1 Point)__ Use `databricks clusters delete <CLUSTER-ID>` to terminate (not actually delete) your cluster. If your cluster is terminated.

______

Take a moment to pat yourself on the back. Using these resources is not easy and you've taken a strong step towards minimizing costs of your Azure learning experience. You may use these tests in your projects however you like to minimize costs. They are marked under the test class `TestClusterIsNotExpensive` in the `4_databricks1_tests.py` file.
_____

#### More about workbooks

- __(+1 Point :`databricks workspace list <Workspace Path>`)__ Add your workspace path to your `databricks_config.json` file in the Cloud Levelup project and create a workbook within that workspace via your webportal. Use the Azure databricks webportal to find the path of your workspace. Another test should pass. Note: this test uses the databricks cli whereas the first test of your ability to create databricks workspaces used the databricks extension of the azure cli. 

- Explore that cli command: what happens if you put the work-__book__ path into the cli command instead of the work-__space__ path? Does that say something about how workbooks are referenced internally?

- Take the following training to get some background on databricks:
    - https://learn.microsoft.com/en-us/training/modules/explore-azure-databricks/
    - https://learn.microsoft.com/en-us/training/modules/use-apache-spark-azure-databricks/
    - https://learn.microsoft.com/en-us/training/modules/perform-data-analysis-azure-databricks/
    - https://learn.microsoft.com/en-us/training/paths/data-engineer-azure-databricks/

Personally, I found it very difficult to do any of the Microsoft exercises with my own account, which is a shame. However, you can accomplish many of them with a small amount of sample data by downloading data from this website: https://raw.githubusercontent.com/MicrosoftLearning/mslearn-databricks/main/data/products.csv. You can't just import the data because it won't be in the DBFS. Instead, go to a workbook, then File>>Upload data to DBFS, and then select your csv. You'll get a path such as "dbfs:/FileStore/Workspace/<etc.>".

- Use this to check that you have correctly uploaded data within a cell of a workbook:
    
    ```
    spark.read.format("csv").option("header", "true").load("dbfs:/FileStore/<address given during upload>")
    ```

- __(+1 Point :`databricks fs ls <filepath>`)__ Add the folderpath (the thing that starts with "dbfs:/") to the `databricks_config.json` in the `dbfs_folderpath` config. If the folder contains a csv file, another test should pass.

#### Summary for Level 4

In this level you created a databricks cluster, workspace, and uploaded a file into the Databricks File System. You also learned how to probe for state via the azure cli and the databricks cli, which is great. You took some Microsoft training and you configured your databrick compute to reduce costs. Good job.

Bonus Content: because you installed the databricks extension and databricks cli, you can now shut down your clusters programmatically. One of your commands is `python do.py shutdown` which will terminate any clusters still active and log you out. The function itself can be found in the `azure_shutdown.py` and `command_files.py` files. Feel free to use them with proper citations.

## Level 5: Connecting Databricks to Storage Containers

Note: I found this to be one of the more complicated steps in setting up my Azure account. Part of the problem is that there are many different possible workflows to connecting databricks and azure storage, so AI models get mixed up if you ask them to help. If you have premium-tier, Microsoft recommends that you use Unity Catalog to manage connections between storage accounts and databricks. If you don't, read on.

FOOTGUN1: Your storage account must be ADLS Gen2 with hierarchical namespaces, etc. if it's not, then you will have errors with credentialing unless you do even more steps. If your prior account was not Gen2, create a second one. Also, make sure that you have hierarchical namesspaces available, and soft delete NOT available.

FOOTGUN2: You have to have some content in your stoage container. It can be a single file, but it must be something for your databricks to interpret.

TL;DR, Databricks are not intrinsically connected to datalakes or any other part of your Azure account. The process of connecting Azure storage to databricks is called "mounting" if you're doing it without Unity Catalog. If you have standard tier, you can't use Unity, so we're going to discuss how to do this for standard tier, although instructions for premium tier and tests related to that workflow can be found at the end of this level.

- Your first step is to learn about about RBAC (Role Based Access Controls) and Service Principals. You can take Microsoft training for these subjects. There are no points associated with this activity though, and we will NOT be using RBAC for this mountt. RBAC is recommended, but we can't associate service principals created in Azure to databricks with standard tier either, so RBAC is out.

Instead, we're going to do the following:
    - Create a "dummy" service principal to get a client-id, client-secret, and tenant-id. This will give us enough credentials to talk to our storage containers.
    - Create an Azure Key Vault and put those data into the keyvault.
    - Create a Key-Vault Backed Secret Scope in Databricks, giving databricks access to our keyvault.
    - (during runtime:) have databricks pull the keys from the keyvault and use those to communicate with the storage account in Azure.
    - With these credentials, mount the storage onto a file system within databricks.
    
#### Registering an Application, Creating a Service Principal for the Application, and Generating an Application Secret (TestServicePrincipalSetup)

This step creates an identity which can interface with services as if it were a user.

- __(+1 Point: `az ad sp list --display-name <databricks_config.json:"databricks_application_display_name">`)__ Register an application with Entra ID. As of this writing, this is available through the Azure Entra ID portal >> Manage >> App registration. This creates an application object. Put the display name in the databricks_config.json file to get your point.

- __(+2 Point: `az role assignment list --scope <your storage account id>`)__ Go to your storage account and give your Service Principal access to your storage account as a Storage Blob Data Contributor.

- __(+1 Point: `az ad app credential list --id <AppId associated with your service principal>`)__ In the same portal, for the same application, go to certificates and secrets and create a secret. __You must document the actual value of the secret because it will never be displayed again!!!__ We'll give you a point if you have a secret associated with the service principal.

### Standard Tier Account

#### Keyvault Creation, Adding Secrets for client-id, tenant-id, and client-secret (TestKeyvaultSetup)

In this step, you need to create a keyvault that securely stores the information that databricks needs to access your storage blobs.

- __(+2 Point: `az keyvault list`)__ In your azure webportal, go to the keyvault page and create a keyvault. This is a place to store security keys. Now add the keyvault Id to the config file in Cloud Levelup.

- __(Points not added yet)__ Add three secrets to the key vault, as follows:

    - secret 1: call it "client-id" and give it a value of the application id (AKA client ID) of your databricks registered app (you can find that in the same window you created your service principal)
    - secret 2: call it "tenant-id" and give it the value of the tenant id in the same place.
    - secret 3: call it "client-secret" and __put the value of the secret you just generated and wrote down__.

- __(+1 Point: `az role assignment list --scope <yourkeyvault id>`)__ Give your Databricks Service Principal (which you just created) a role that can use key vault secrets using IAM (try Key Vault Secret User). In AIM, when you're assigning a member, your Service Principal should be listed under its display name as if it were a user.

#### Creating an Azure Key Vault-backed secret scope in databricks

- __(+2 Point: `az role assignment list --scope <keyvault id>`)__ Put your keyvault Id in the config file after you use IAM to give your service principal the role of a Key Vault Secret User in your keyvault. One point for adding the correct keyvault to the config file, and one point for giving the application service principal the correct role.

- __(+2 Points: `databricks secrets list-scopes`)__ Go to https://<databricks-instance>/#secrets/createScope. Enter the name of the secret scope (anything you want), select manage principal for all workspace users, the DNS name of your keyvault, and the Resource ID of your keyvault. You get a point if you can create a scope, and another point if it has a type of Azure Keyvault. I think of this as databricks "borrowing" the security afforded by Azure keyvaults.

#### Checking that your databricks account can get access to the key-vault secrets.

Run this in a workspace:

```
my_scope = "<your secret scope>"
tenant_id = dbutils.secrets.get(scope=my_scope, key="tenant-id")
client_secret = dbutils.secrets.get(scope=my_scope, key="client-secret")
client_id = dbutils.secrets.get(scope=my_scope, key="client-id")
```

If that doesn't error, then your databricks workspace has access to your keyvault secrets. This step insures that you are able to access the secrets in your keyvault.

Then run this to get a sense of what mounts are:
```
mount_point = "/mnt/<the foldername you want to use to access your storage container>"
for m in dbutils.fs.mounts():
    print(m.mountPoint)
try:
    dbutils.fs.unmount(mount_point)
except:
    pass
```

Then run this:
```
account     = "<your storage account name>"
container   = "<your container name>" #must be second gen, must not have blob soft delete, must have content
abfss       = f"abfss://{container}@{account}.dfs.core.windows.net/"
configs     = {
    "fs.azure.account.auth.type" : "OAuth",
    "fs.azure.account.oauth.provider.type" : "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id" : client_id,
    "fs.azure.account.oauth2.client.secret" : client_secret,
    "fs.azure.account.oauth2.client.endpoint" : f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
}

dbutils.fs.mount(
    source          = abfss,
    mount_point     = mount_point,
    extra_configs   = configs
)

display(dbutils.fs.ls(mount_point))
```

At this point, debug like crazy. You're probably going to need to redo these steps a couple of times.

#### Level 5 Summary

In this level, you mounted your Azure storage blob container onto your databricks file system (DBFS). At a company or institution, this will likely be done for you. However, now you know how to troubleshoot, debug, and request reconfigurations. This will also allow you to complete more of the exercises in Azure training without needing to do their setups.