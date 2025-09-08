
az costmanagement export create \
--scope "$1" \
--name "$2" \
--storage-container "$4" \
--storage-account-id "$3" \
--timeframe "MonthToDate" \
--storage-directory "$5" \
--type Usage \
--output json