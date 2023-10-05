terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.33.0"
    }
  }
}

provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {}
}

variable "prefix" {
  default = "th"
  type = string
}

resource "azurerm_resource_group" "rg" {
  name = "${var.prefix}-rg"
  location = "East US"
}

resource "azurerm_storage_account" "storage" {
  name = "${var.prefix}storage981357"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  account_kind = "StorageV2"
  account_tier = "Standard"
  account_replication_type = "LRS"
  infrastructure_encryption_enabled = true

  blob_properties {
    versioning_enabled = true
  }
}

resource "azurerm_storage_container" "container" {
  name = "files"
  storage_account_name = azurerm_storage_account.storage.name
}
