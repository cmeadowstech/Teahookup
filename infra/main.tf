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
  container_access_type = "blob"
}

#############################################################################################
#                                                                                           #
# CDN Endpoint for Storage Account                                                          #
# https://ssmertin.com/articles/exposing-azure-storage-on-domain-apex-with-letsencrypt-ssl/ #
#                                                                                           #
# NOTE: Need to test SSL before deploying to prod                                           #
#                                                                                           #
#############################################################################################

/*

resource "azurerm_cdn_profile" "cdn-p" {
  name = "${var.prefix}-cdn"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  tags = azurerm_resource_group.rg.tags
  sku = "Standard_Microsoft"
}

resource "azurerm_cdn_endpoint" "cdn-ep" {
  name = "${var.prefix}-edge"
  profile_name = azurerm_cdn_profile.cdn-p.name
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  origin_host_header = azurerm_storage_account.storage.primary_web_host

  origin {
    name = "origin"
    host_name = azurerm_storage_account.storage.primary_web_host
  }

  delivery_rule {
    name  = "EnforceHTTPS"
    order = 1

    request_scheme_condition {
      operator = "Equal"
      match_values = ["HTTP"]
    }

    url_redirect_action {
      redirect_type = "Found"
      protocol = "Https"
    }
  }
}

*/