# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.27.0"
    }
  }
  required_version = ">= 0.14"
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
  #skip_provider_registration = true

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.appId
  client_secret   = var.password
}

# Declare the missing data source
data "azurerm_client_config" "current" {}

# ------------------------------------------------------------------------------------------------------
# Generate a random prefix for resource names
# ------------------------------------------------------------------------------------------------------
resource "random_pet" "prefix" {}

# ------------------------------------------------------------------------------------------------------
# Deploy Resource Group
# ------------------------------------------------------------------------------------------------------
resource "azurerm_resource_group" "clipsify" {
  name     = "clipsify-rg"
  location = "germanywestcentral"

  tags = {
    environment = "Dev"
  }
}

# ------------------------------------------------------------------------------------------------------
# Generate a resource token
# ------------------------------------------------------------------------------------------------------
locals {
  sha            = base64encode(sha256("${azurerm_resource_group.clipsify.tags["environment"]}${azurerm_resource_group.clipsify.location}${data.azurerm_client_config.current.subscription_id}"))
  resource_token = substr(replace(lower(local.sha), "[^A-Za-z0-9_]", ""), 0, 13)
}

# ------------------------------------------------------------------------------------------------------
# Deploy Azure Container Registry
# ------------------------------------------------------------------------------------------------------
resource "azurerm_container_registry" "clipsify" {
  name                = "${replace(random_pet.prefix.id, "-", "")}acr"
  resource_group_name = azurerm_resource_group.clipsify.name
  location            = azurerm_resource_group.clipsify.location
  sku                 = "Basic"
  admin_enabled       = false
  tags = {
    environment = "Dev"
  }
}

# ------------------------------------------------------------------------------------------------------
# Deploy AKS cluster
# ------------------------------------------------------------------------------------------------------
resource "azurerm_kubernetes_cluster" "clipsify" {
  name                = "${random_pet.prefix.id}-aks"
  location            = azurerm_resource_group.clipsify.location
  resource_group_name = azurerm_resource_group.clipsify.name
  dns_prefix          = "${random_pet.prefix.id}-k8s"
  kubernetes_version  = "1.32.0"

  default_node_pool {
    name            = "default"
    node_count      = 2
    vm_size         = "Standard_D2as_v6"
    os_disk_size_gb = 30
  }

  service_principal {
    client_id     = var.appId
    client_secret = var.password
  }

  role_based_access_control_enabled = true

  tags = {
    environment = "Dev"
  }
}

# ------------------------------------------------------------------------------------------------------
# Deploy application insights
# ------------------------------------------------------------------------------------------------------
module "applicationinsights" {
  source           = "./modules/applicationinsights"
  location         = azurerm_resource_group.clipsify.location
  rg_name          = azurerm_resource_group.clipsify.name
  environment_name = "${random_pet.prefix.id}-ai"
  workspace_id     = module.loganalytics.LOGANALYTICS_WORKSPACE_ID
  tags             = azurerm_resource_group.clipsify.tags
  resource_token   = local.resource_token
}

# ------------------------------------------------------------------------------------------------------
# Deploy log analytics
# ------------------------------------------------------------------------------------------------------
module "loganalytics" {
  source         = "./modules/loganalytics"
  location       = azurerm_resource_group.clipsify.location
  rg_name        = azurerm_resource_group.clipsify.name
  tags           = azurerm_resource_group.clipsify.tags
  resource_token = local.resource_token
}