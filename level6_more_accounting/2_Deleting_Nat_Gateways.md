## NAT Gateways and Resource Management

---

You may have notices that your resource group contains some resources that you didn't explicitly create. This is because the configurations of the resources provisioned in earlier exercises authorized the creation of additional hidden resources. Some of these resources cost money even when idle, deactivated, or otherwise unused. To use Azure responsibly, you must understand the costing model for each of these resource types, and their relationship to one another.

NAT Gateways cost money even when they aren't active. This is bad for learning. This task will help you recreate a databricks workspace so that it does not require private-to-public communication, and therefore does not require a NAT gateway. You don't need to do this task if already have NAT-less databricks workspaces.

https://learn.microsoft.com/en-us/azure/nat-gateway/manage-nat-gateway?tabs=manage-nat-portal

Public IP Addresses cost additional money under most conditions, but it is generally much less expensive than a NAT Gateway (~$2/mo). We will be focusing on minimizing the costs of public IP addresses later.

#### Understanding NAT Gateways and Subnets

First we need to understand NAT gateways. While NAT gateways may be required for your employer's setup, they are not necessary in a learning environment. Go learn about NAT gateways here:
- https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview.
- https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/secure-cluster-connectivity#egress-with-default-managed-vnet.

Here is the metaphor: a VNet is a city (a collection of IpAddresses and other infrastructure). A subnet is a borrough. A NAT gateway allows a borrough to be __only__ private and to interface with the public. It is like putting a gate around the borrough, turning it into a gated community. Every subnet has a private IP address (this is a requirement by Microsoft), some have public IP addresses, but the ones with only private IP addresses need a NAT gateway to communicate with the public internet.

Another way of saying this is, when you create a workspace in databricks, you don't really create much other than configurations. However, you set whether you want your workspace to have a public Ip address or not. If it doesn't, then it either needs to be communicating privately, within the community, or it needs to use a Nat.

---

#### How are Databricks Workspaces associated to Nat Gateways?

Answer: when a Databricks Workspace provisions a cluster of virtual machines, the VMs create network interfaces to talk to the internet. The cluster uses the interface to communicate on the subnet, which may or may not require a NAT to complete these communications. Here is the key: the cluster needs a subnet regardless of where it is communicating, but it only needs a NAT if the subnet is supposed to be private and the databricks workspace is configured to communicate with public IPs. This leaves us with three options:

1. Databricks Public IP address <--> Blob storage Public Endpoint/IP (easy configuration, cheaper, and unsecure)
2. Databricks No Public IP address + NAT gateway <--> Blob storage public endpoint/IP (easy configuration, more expensive, and secure)
3. Databricks No Public IP address, No NAT gateway <--> Blob storage private endpoint (hard configuration, cheap(est?), and secure)

So we basically need to make sure our Databricks workspaces are either 1 or 3, and avoid 2.

__(+1 Point, test 5)__ Have a free point. You made it this far.

__(+1 Point, test 6)__ It's difficult to find out which databricks workspace is associated with which NAT because the association is not clear until you provision a virtual machine to run a cluster. So, for now, let's just explore KQL results of the `network.natgateways` resource. Query that resource and return a result with the following to collect a point:

- it must have at least five pieces/columns of data, some of which can be json objects or lists
- include the id column and name column.
- include the tags attribute, which you must call "tags"
- include the subnets attribute, which you must call "subnets"
- include the public IP addresses attribute, which you must call "public_ip_addresses"

Now examine that result: which of your nats are associated with databricks? How can you tell?

Answer: the tags section has a tag which identifies a NAT gateway as using databricks. This occurs when the NAT gateway is provisioned automatically by your db workspace setup configuration (ie, not by you but by Microsoft). This thing costs money, and we don't really need it for now.

---

__(+1 Point, test 7)__ For now, just put a query of the `microsoft.compute.virtualmachines` resource. It may return nothing.

__(+1 Point, test 8)__ For now, just put a query of the `network.networkinterfaces` resource. It may return nothing as well.

---

Now run an experiment:

1) If you haven't already done so, create a completely new databricks workspace with your Azure portal that __allows a public IP address__, and configure some cheap compute for it. Rerun queries 4, 6, 7, and 8. You should see two workspaces, and depending on what you have running, you may see VMs and network interfaces as well.

2) Turn on your compute for your new workspace and make sure you can mount the blob storage that you mounted in levels 4 and 5.

3) Now delete the databricks workspace which does not have an IP address by using the Azure portal. You may need to turn its cluster off first.

You should observe: 1) the number of workspaces in query3 decreasing by one, 2) the number of nat gateways decreasing by one as well, despite not having deleted the NAT gateway explicitly, 3) the number of virtual machines decreasing by one, and 4) the number of network interfaces decreasing by two.

Check that you can still mount your blob storage with your new workspace, despite it not having a NAT.