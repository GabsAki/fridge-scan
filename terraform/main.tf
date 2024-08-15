provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  name     = "MyResourceGroup"
  location = "East US"
}

# Create an App Service Plan
resource "azurerm_app_service_plan" "asp" {
  name                = "MyAppServicePlan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "Linux"
  reserved            = true

  sku {
    # tier = "Free"
    # size = "F1"
    tier = "Basic"
    size = "B1"
  }
}

# Create an Azure Key Vault
resource "azurerm_key_vault" "kv" {
  name                = "fridgeScanKeyVault"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
      "Recover",
      "Restore",
    ]
  }
}

resource "azurerm_key_vault_access_policy" "app_access_policy" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id

  # Reference the object_id of the managed identity associated with the web app
  object_id = azurerm_linux_web_app.app.identity[0].principal_id

  secret_permissions = [
    "Get",
    "List",
    "Set",
    "Delete",
    "Recover",
    "Restore",
  ]
}

# Store the secret in the Key Vault
resource "azurerm_key_vault_secret" "openai_secret" {
  name         = "OPENAI-KEY"
  value        = "REPLACE" # Replace with your actual secret
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "freeimage_secret" {
  name         = "FREEIMAGE-API-KEY"
  value        = "REPLACE" # Replace with your actual secret
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "google_secret" {
  name         = "GOOGLE-API-KEY"
  value        = "REPLACE" # Replace with your actual secret
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_linux_web_app" "app" {
  name                = "fridge-scan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id = azurerm_app_service_plan.asp.id

  site_config {
    always_on = false

    application_stack {
        docker_image_name = "gabsaki/fridge-scan"
        docker_registry_url = "https://index.docker.io"  # URL for Docker Hub
    }
  }

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    WEBSITES_PORT                       = "8000"
    OPENAI_KEY                          = azurerm_key_vault_secret.openai_secret.value
    FREEIMAGE_API_KEY                   = azurerm_key_vault_secret.freeimage_secret.value
    GOOGLE_API_KEY                      = azurerm_key_vault_secret.google_secret.value
  }

  lifecycle {
    ignore_changes = [
      app_settings["WEBSITES_ENABLE_APP_SERVICE_STORAGE"]
    ]
  }

  identity {
    type = "SystemAssigned"
  }
}

# Output the URL of the web app
output "app_url" {
  value       = azurerm_linux_web_app.app.default_hostname
  description = "The URL of the deployed FastAPI application"
}
