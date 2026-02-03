#!/bin/bash

# Script to cleanup Azure resources for the Todo application
# Used for task T072: Create cleanup verification script to check resource group deleted

RESOURCE_GROUP=${1:-"todo-rg"}

echo "Starting Azure resource cleanup..."

# Check if az command exists
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI (az) is not installed or not in PATH"
    exit 1
fi

# Check if resource group exists
if az group exists --name "$RESOURCE_GROUP" 2>/dev/null; then
    echo "Resource group '$RESOURCE_GROUP' found. Initiating deletion..."

    # Delete the resource group (this will delete all resources within it)
    az group delete --name "$RESOURCE_GROUP" --yes --no-wait

    echo "Deletion initiated. Resource group and all contained resources will be deleted asynchronously."
else
    echo "Resource group '$RESOURCE_GROUP' not found. Already deleted or never created."
fi

# Wait a moment for the deletion to start
sleep 10

# Verify deletion
if ! az group exists --name "$RESOURCE_GROUP" 2>/dev/null; then
    echo "SUCCESS: Resource group '$RESOURCE_GROUP' has been deleted or deletion is in progress."
else
    echo "WARNING: Resource group '$RESOURCE_GROUP' still exists."
fi

echo "Cleanup process completed."