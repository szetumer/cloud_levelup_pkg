## NAT Gateways and Resource Management

You may have notices that your resource group contains some resources that you didn't explicitly create. This is because the configurations of the resources provisioned in earlier exercises authorized the creation of additional hidden resources. Some of these resources cost money even when idle, deactivated, or otherwise unused. To use Azure responsibly, you must understand the costing model for each of these resource types.

NAT Gateways cost money even when they aren't active. This is bad for learning. This task will help you recreate a databricks workspace so that it does not require private-to-public communication, and therefore does not require a NAT gateway. You don't need to do this task if already have NAT-less databricks workspaces.

Public IP Addresses cost additional money under most conditions, but it is generally much less expensive than a NAT Gateway. We will be focusing on minimizing the costs of public IP addresses later.

#### Understanding NAT Gateways

First we need to understand NAT gateways. While NAT gateways may be required for your employer's setup, they are not necessary in a learning environment. Go learn about NAT gateways here:
- https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview.
- https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/secure-cluster-connectivity#egress-with-default-managed-vnet.

I think of NAT gateways as the gates of a gated community, whose addresses are a VNet in this analogy. Within the community, you're communicating on Microsoft's private network. The borroughs of the community are different subnets. The NAT gateway is how you interface with the public internet. This means we have three options for connecting our databricks workspace to the rest of our storage account.

1. Databricks Public IP address <--> Blob storage Public Endpoint/IP (easy configuration, cheaper, and unsecure)
2. Databricks No Public IP address + NAT gateway <--> Blob storage public endpoint/IP (easy configuration, more expensive, and secure)
3. Databricks No Public IP address, No NAT gateway <--> Blob storage private endpoint (hard configuration, cheap(est?), and secure)

We will be using our KQL to query our resource graph to identify places where you accidentally chose option 2s and recreate them so that they are option 1s instead.

__(+1 Point)__ Disable tests 0 through 4. You won't need those for this section.

__(+1 Point, test 6)__ We need to find the databrick workspaces which have a Nat gateway. In this KQL query, first explore the attributes of the nat gateways associated with your account, then write a query so that the result contains the following information: 

