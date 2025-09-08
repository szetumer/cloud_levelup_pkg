BillingProfile=$1
ReportName=$2
StorageAccountId=$3
StorageContainerName=$4
StorageDirectory=$5

echo $BillingProfile
echo $ReportName
echo $StorageAccountId
echo $StorageContainerName
echo $StorageDirectory

az costmanagement export create \
--scope "$1" \
--name "$ReportName" \
--storage-container "$StorageContainerName" \
--storage-account-id "$StorageAccountId" \
--timeframe "MonthToDate" \
--storage-directory "$StorageDirectory" \
--type Usage \
--output json