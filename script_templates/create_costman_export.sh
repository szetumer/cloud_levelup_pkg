set BillingVariable = $1
set ReportName = $2
set StorageAccountId = $3
set StorageContainerName = $4
set StorageDirectory = $5

az costmanagement export create /
--scope $BillingVariable /
--name MyUsageExport /
--storage-container $StorageContainerName ^
--storage-account-id $StorageAccountId ^
--timeframe MonthToDate ^
--storage-directory $StorageDirectory ^
--type Usage ^
--output json