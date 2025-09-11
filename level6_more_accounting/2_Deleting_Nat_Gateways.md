#### Querying Nat Gateways

You may have notices that your resource group contains some resources that you didn't explicitly create. This is because the configurations of the resources provisioned in earlier exercises authorized the creation of these resources. Some of these resources cost money even when idle, deactivated, or otherwise unused. To use Azure responsibly, you must understand the costing model for each of these resources, part of which is deleting these unused resources.

First we need to understand NAT gateways. Then we need to get rid of them.

__(+1 Point, test 5)__ We need to find the databrick workspaces which have a Nat gateway. In this KQL query, first explore the attributes of the nat gateways associated with your accounts.

