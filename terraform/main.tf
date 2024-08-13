# main.tf

provider "azurerm" {
  features {}
}

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
    tier = "Free"
    size = "F1"
  }
}

# Create the Web App
# Create the Linux Web App
resource "azurerm_linux_web_app" "app" {
  name                = "fridge-scan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id = azurerm_app_service_plan.asp.id

  site_config {
    always_on = false

    application_stack {
        docker_image_name = "gabsaki/fridge-scan"
    }
  }

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    WEBSITES_PORT                       = "8000"
  }

  lifecycle {
    ignore_changes = [
      app_settings["WEBSITES_ENABLE_APP_SERVICE_STORAGE"]
    ]
  }
}

# Output the URL of the web app
output "app_url" {
  value       = azurerm_linux_web_app.app.default_hostname
  description = "The URL of the deployed FastAPI application"
}
