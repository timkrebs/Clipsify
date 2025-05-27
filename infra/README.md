# Provision AKS Cluster

This repo is a companion repo to the [Provision an AKS Cluster tutorial](https://developer.hashicorp.com/terraform/tutorials/kubernetes/aks), containing Terraform configuration files to provision an AKS cluster on Azure.


## Create an Active Directory service principal account
There are many ways to authenticate to the Azure provider. In this tutorial, you will use an Active Directory service principal account. You can learn how to authenticate using a different method here.

First, you need to create an Active Directory service principal account using the Azure CLI. You should see something like the following.
```bash
$ az ad sp create-for-rbac --skip-assignment
{
  "appId": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "displayName": "azure-cli-2019-04-11-00-46-05",
  "name": "http://azure-cli-2019-04-11-00-46-05",
  "password": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "tenant": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
}
```

## Update your terraform.tfvars file
Replace the values in your terraform.tfvars file with your appId and password. Terraform will use these values to authenticate to Azure before provisioning your resources. Your terraform.tfvars file should look like the following.

## terraform.tfvars
```
appId    = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
password = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
```

## Initialize Terraform
After you have saved your customized variables file, initialize your Terraform workspace, which will download the provider and initialize it with the values provided in your terraform.tfvars file.

```
$ terraform init
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/azurerm from the dependency lock file
- Reusing previous version of hashicorp/random from the dependency lock file
- Installing hashicorp/azurerm v3.67.0...
- Installed hashicorp/azurerm v3.67.0 (signed by HashiCorp)
- Installing hashicorp/random v3.5.1...
- Installed hashicorp/random v3.5.1 (signed by HashiCorp)

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.
```

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

Provision the AKS cluster
In your initialized directory, run terraform apply and review the planned actions. Your terminal output should indicate the plan is running and what resources will be created.

### Note
If you get an error that the VM size of Standard_D2_v2 is not allowed in your subscription, you may have reached a resource limit. Refer to the AKS VM size restrictions and region availability documentation for more information.

```bash
$ terraform apply
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
```

You can see this terraform apply will provision an Azure resource group and an AKS cluster. Confirm the apply with a yes.

This process should take approximately 5 minutes. Upon successful application, your terminal prints the outputs defined in aks-cluster.tf.

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
```
Outputs:
kubernetes_cluster_name = light-eagle-aks
resource_group_name = light-eagle-rg
```

## Configure kubectl
Now that you've provisioned your AKS cluster, you need to configure kubectl.

Run the following command to retrieve the access credentials for your cluster and automatically configure kubectl.

```bash
$ az aks get-credentials --resource-group $(terraform output -raw resource_group_name) --name $(terraform output -raw kubernetes_cluster_name)
Merged "light-eagle-aks" as current context in /Users/dos/.kube/config
```

The resource group name and Kubernetes Cluster name correspond to the output variables showed after the successful Terraform run.

## Access Kubernetes Dashboard
To verify that your cluster's configuration, visit the Azure Portal's Kubernetes resource view. Azure recommends using this view over the default Kubernetes dashboard, since the AKS dashboard add-on is deprecated for Kubernetes versions 1.19+.

Run the following command to generate the Azure portal link.

```bash
$ az aks browse --resource-group $(terraform output -raw resource_group_name) --name $(terraform output -raw kubernetes_cluster_name)
```

Go to the URL in your preferred browser to view the Kubernetes resource view.

