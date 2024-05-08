



### Connect to an AKS Cluster With Azure CLI and Kubectl


To connect to an  Azure AKS cluster, first, we need to login to  Azure using the following command:

```powershell
az login
```
If you have more than one subscription, set it using the following command:

```powershell	
az account set --subscription subname 
```
After login to Azure, install the Kubectl command line tools plug-in for Azure CLI using the following line:

```powershell	
az aks install-cli
```
Finally, we run the following command to authenticate to our AKS cluster. Make sure you fill in the resource group name of your cluster and your cluster name:

```powershell
az aks get-credentials --resource-group RGNAME --name CLUSTERNAME
```

You can type kubectl, access the help file, and start managing your AKS cluster.