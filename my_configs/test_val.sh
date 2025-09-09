
az costmanagement export create \
--scope "/providers/Microsoft.Billing/billingAccounts/0ff0687b-bc43-5408-e09a-d53137bfff96:0adc693c-8172-4ad8-a64b-14073142f093_2019-05-31/billingProfiles/IM4X-4HIU-BG7-PGB" \
--name "MyUsageExportV2" \
--storage-container "szlearningstoragecontainer" \
--storage-account-id "/subscriptions/c089d3c0-ebe2-49d9-ad1c-0a968ee41e55/resourceGroups/SZLearningResourceGroup/providers/Microsoft.Storage/storageAccounts/szlearningstorageaccount" \
--timeframe "MonthToDate" \
--storage-directory "CostReports" \
--type Usage \
--output json 