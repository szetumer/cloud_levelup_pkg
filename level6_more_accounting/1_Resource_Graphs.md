#### Learning KQL (Kusto Query Language)

__(+1 Point)__ So for this level, we're going to discuss various ways of keeping costs low. Our first way will be to install the resource-graph extension for the azure cli.

(No points but you need to do this) Read about KQL. It will make automating the auditing of resource consumption easier. Use these tutorials:
    - https://learn.microsoft.com/en-us/azure/governance/resource-graph/samples/starter?tabs=azure-cli
    - https://learn.microsoft.com/en-us/kusto/query/tutorials/learn-common-operators?view=azure-data-explorer&preserve-view=true
    - https://dataexplorer.azure.com/clusters/help/databases/Samples

__(+1 Point)__ go to the [Azure Resource Graph Explorer](https://learn.microsoft.com/en-us/azure/governance/resource-graph/first-query-portal) and noodle around. Make sure that the scope listed in the top left of the leftmost blade says "Subscription" and then lists your subscription. Create a KQL query that works in this portal, using single quotes for any quotations. Cut and paste it into query 1 in the `rgraph_queries.json` file in Cloud Levelup to claim your point. That query must return a valid result via the azure cli to get the point. (NB: we're going to check that you have a "count" field in your query result so just keep the query simple. Most queries return a count if returned in json format)

NOTE: these results may get big, so many of the results will be dumped into files that go into the `my_reports` folder. Inspect your results to review your work!

You can use these as KQL guides:
- https://www.bing.com/videos/riverview/relatedvideo?&q=Learning+Microsoft+Azure+KQL&&mid=1887D20FC10C9E1EB9611887D20FC10C9E1EB961&&FORM=VRDGAR

Here are some useful queries. Activate these tests to get those points:

__(+1 Point for activating test 2)__ `resources | summarize by type | sort by type asc`. Look at the results in the `my_reports` folder. Those are all the resources you can query. __This query result is very important for understanding costs__. Many of these resources cost you money. As you provision more resources, this list will expand.

__(+1 Point, test 3)__ list all your databricks workspaces as a query result. Return whatever columns you want, and the results will appear in `query3_workspace_attrs.json`. Use this to understand what attributes are associated with each databricks workspace.

To collect the equivalent amount of data without using KQL, we have to the following cli commands:

- use `az group list` to get the name of all resource groups associated with your subscription.
- for each of these resource group names, run `az databricks workspace --resource-group <resource group name>`. Sum up the length of the results.

Notice that this test runs very slowly. KQL queries of the resource graph are much more efficient than using the Azure cli without the query. I recommend disabling this query after you get this test to pass so that your tests don't run slowly for the rest of this level.

__(+1 Point, test 4)__ Write a query which returns your databrick workspaces associated with your subscription, and project the columns of "name", "id", and the parameters subsection. Note that name and id are strings, but parameters is a json object. NB: this is why we return our result as json objects - it allows us to appreciate the nested information contained in our results. Your columns should be labelled "id", and "properties_parameters". The last column should return a dictionary of information.

Additional exercises, no points: learn how to use mv-expand in KQL.