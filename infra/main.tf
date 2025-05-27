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
  resource_provider_registrations = "all"

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.appId
  client_secret   = var.password
}

resource "random_pet" "prefix" {}

resource "azurerm_resource_group" "clipsify" {
  name     = "clipsify-rg"
  location = "germanywestcentral"

  tags = {
    environment = "Dev"
  }
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

