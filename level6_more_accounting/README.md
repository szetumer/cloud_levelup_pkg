## Level 6: Cleaning Up Resources

NOTE: Throughout this level, you may get a warning that your query has failed due to throttling. This is because you are placing too much demand on the public API, and they are refusing to run your query. If that is the case, simply skip the queries that are causing your requests to be throttled by deleting those test numbers from the `tests_to_run` parameter in `rgraph_queries.json` file.

IMHO, Azure doesn't do a very good job helping you keep costs __extremely__ low. They're more of a B2B operation than a B2C operation, which makes training difficult because you could spend an extra $20 without realizing it. That's not a big deal for a company, but if you're doing this on your own dime and with your own time, that can sting and keep motivation low.

As an additional motivation, consider this: if you figure out how to shave off 1% of your company's costs from their Azure bill, you could likely pay for your own salary.

(+1 Point) So for this level, we're going to discuss various ways of keeping costs low. Our first way will be to install the resource-graph extension for the azure cli.

(No points but you need to do this) Read about KQI. It will make automating the auditing of resource consumption easier. Use these tutorials:
    - https://learn.microsoft.com/en-us/azure/governance/resource-graph/samples/starter?tabs=azure-cli
    - https://learn.microsoft.com/en-us/kusto/query/tutorials/learn-common-operators?view=azure-data-explorer&preserve-view=true
    - https://dataexplorer.azure.com/clusters/help/databases/Samples

(+1 Point) go to the [Azure Resource Graph Explorer](https://learn.microsoft.com/en-us/azure/governance/resource-graph/first-query-portal) and noodle around. Make sure that the scope listed in the top left of the leftmost blade says "Subscription" and then lists your subscription. Create a KQI query that works in this portal, using single quotes for any quotations. Cut and paste it into query 1 in the `rgraph_queries.json` file to claim your point. That query must return a valid result via the azure cli to get the point. (NB: we're going to check that you have a "count" field in your query result so just keep the query simple. Most queries return a count if returned in json format)

NOTE: these results may get big, so many of the results will be dumped into files that go into the `my_reports` folder. Inspect your results to review your work!

Here are some useful queries. Activate these tests to get those points:

(+1 Point for activating test 2) `resources | summarize by type | sort by type asc`

(+1 Point, test 3) list all your databricks workspaces as a query result. Return whatever columns you want, and the results will appear in `query3_workspace_attrs.json`. Use this to understand what attributes are associated with each workspace.

To collect the equivalent amount of data without using the query system, we have to the following cli commands:

- use `az group list` to get the name of all resource groups associated with your subscription.
- for each of these resource group names, run `az databricks workspace --resource-group <resource group name>`. Sum up the length of the results.

Notice that this query runs very slowly. KQI queries are much more efficient than using the Azure cli without the query. I recommend disabling this query after you get this test to pass so that your tests don't run slowly for the rest of this level.
