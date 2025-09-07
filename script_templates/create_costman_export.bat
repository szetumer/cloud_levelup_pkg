@echo off
:: Define variables
set BillingVariable = %1
set ReportName = %2
set StorageAccountId = %3
set StorageContainerName = %4
set StorageDirectory = %5

az costmanagement export create ^
:: use billing account profile for this one
--scope %1% ^ 
--name MyUsageExport ^
--storage-container %4% ^ 
:: remember to use storage account tsv
--storage-account-id %3% ^
--timeframe MonthToDate ^
--storage-directory %2% ^
--type Usage ^
--output json