from src.cloud_levelup.command_files import GetAzure

def azure_shutdown():
    j : list[dict] = GetAzure._json("databricks", "clusters", "list", "--output", "json")
    print("The following compute clusters were checked:")
    for d in j:
        print(d["cluster_id"])
    print("___________SHUTTING DOWN CLUSTERS:___________")
    for d in [d for d in j if d["state"] != "TERMINATED"]:
        print(GetAzure._json("databricks", "clusters", "delete", d["cluster_id"], "--output", "json"))
    print("___________LOGGING OUT USER:___________")
    print(GetAzure._json("az", "logout", "--output", "json"))
    print("___________COMPLETED AZURE SHUTDOWN PROCESS___________")