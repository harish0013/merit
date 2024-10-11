class Field_List():
    
    expected_fields = [
    'Make', 'Model', 'Trim', 'Derivative', 'Derivative_Translated_English', 'Number_Of_Doors',
    'Body_Type', 'Power_Train', 'Version_Name', 'Version_Name_Translated_English', 'Manufacturer_S_Code',
    'Configurator_Model_Year', 'Built_Option_Pack', 'Uid', 'Data_Date', 'Conclude_Date',
    'Version_Availability', 'Currency', 'Price', 'Delivery_Costs_Retail', 'Cost_To_Return_The_Vehicle_Retail',
    'Total_Mandatory_Packs_Amount', 'Country', 'Research_Date', 'Start_Date', 'End_Date', 'Customer_Type',
    'Monthly_Payment_Type', 'Product_Name', 'Product_Description', 'Monthly_Payment_Provider_Name',
    'Monthly_Payment_Provider_Type', 'Interest_Rate_Apr', 'Interest_Rate_Nominal', 'Contract_Duration_Months',
    'Yearly_Mileage_Km', 'Yearly_Mileage_Miles', 'Total_Contract_Mileage_Km', 'Total_Contract_Mileage_Miles',
    'Deposit_Percentage_Of_Price', 'Deposit_Retail', 'Deposit_Base','Of_Monthly_Payments_In_Advance', 'Of_Monthly_Instalments',
    'First_Monthly_Instalment_Amount_Retail', 'First_Monthly_Instalment_Amount_Base',
    'Regular_Monthly_Instalment_Amount_Retail', 'Regular_Monthly_Instalment_Amount_Base', 'Additional_Fees_Retail',
    'Additional_Fees_Base', 'Final_Payment_Type', 'Final_Payment_Percentage_Of_Price', 'Final_Payment_Retail',
    'Final_Payment_Base','Data_Source', 'Web_Source_Url', 'Advertised_Price_Point_Monthly_Payment',
    'Published_Start_Date', 'Published_End_Date', 'Oem_Web_Financial_Configurator_Source',
    'Captive_Financial_Configurator_Source', 'Non_Captive_Financial_Configurator_Source',
    'Bank_Financial_Configurator_Source', 'Sourced_Dealer_Quote', 'Jato_Internal_Source', 'Other_Sources',
    'Vehicle_Price_Reference', 'Mandatory_Dealer_Contribution_Percentage_Of_Price', 'Mandatory_Dealer_Contribution_Retail',
    'Mandatory_Dealer_Contribution_Base', 'Oem_Discount_Percentage_Of_Price', 'Oem_Discount_Retail', 'Oem_Discount_Base',
    'Government_Contribution_Percentage_Of_Price', 'Government_Contribution_Retail', 'Government_Contribution_Base',
    'Downpayment_Allowance_Percentage_Of_Price', 'Downpayment_Allowance_Retail', 'Downpayment_Allowance_Base',
    'Captive_Rebate_Percentage_Of_Price', 'Captive_Rebate_Retail', 'Captive_Rebate_Base', 'Free_Supply_Amount',
    'Residual_Value_Percentage_Of_Price', 'Residual_Value_Retail', 'Residual_Value_Base', 'Lease_Factor_Index',
    'Insurance', 'Theft_And_Fire_Insurance', 'Insurance_Description', 'Sourced_Financed_Amount_Percentage_Of_Price',
    'Sourced_Financed_Amount_Retail', 'Sourced_Financed_Amount_Base', 'Unique_Id', 'Change_Status',
    'Updates_Column', 'Back_End_Data', 'Vehicle_Hash', 'Excess_Mileage_Retail', 'Excess_Mileage_Base',
    'Reimbursement_Mileage_Retail', 'Reimbursement_Mileage_Base', 'Courtesy_Car', 'Courtesy_Car_Description',
    'Courtesy_Car_Duration_Months', 'Courtesy_Car_Amount', 'Fuel_And_Electric_Supply', 'Fuel_And_Electric_Supply_Description',
    'Supply_Duration_Months', 'Supply_Amount', 'Fuel_Quantity_L', 'Fuel_Quantity_Gal', 'Electricity_Quantity_Kw',
    'Road_Assistance', 'Road_Assistance_Description', 'Road_Assistance_Duration_Months', 'Road_Assistance_Distance_Km',
    'Road_Assistance_Distance_Miles', 'Road_Assistance_Amount', 'Flexible_Early_Cancellation_Possible',
    'Notice_To_Terminate_The_Contract_Mths', 'Cost_To_Terminate_Contract_Percentage_Of_Price',
    'Cost_To_Terminate_The_Contract_Retail', 'Cost_To_Terminate_The_Contract_Base', 'Cost_To_Terminate_The_Contract_Description',
    'Road_Tax', 'Tyres', 'Tyres_Description', 'Tyres_Duration_Months', 'Of_Summer_Tyres', 'Of_Winter_Tyres',
    'Of_All_Seasons_Tyres', 'Tyres_Amount', 'Premium_Tyres', 'Tyres_Storage_Service', 'Maintenance',
    'Maintenance_Description', 'Maintenance_Duration_Months', 'Maintenance_Distance_Km', 'Maintenance_Distance_Miles',
    'Maintenance_Amount', 'Repair', 'Repair_Description', 'Repair_Duration_Months', 'Repair_Distance_Km',
    'Repair_Distance_Miles', 'Repair_Amount', 'Service', 'Service_Description', 'Service_Duration_Months',
    'Service_Distance_Km', 'Service_Distance_Miles', 'Service_Amount'
]

    cost_related_fields = [
        'Price', 'Delivery_Costs_Retail', 'Cost_To_Return_The_Vehicle_Retail', 'Total_Mandatory_Packs_Amount',
        'Deposit_Retail', 'Deposit_Base', 'First_Monthly_Instalment_Amount_Retail', 'First_Monthly_Instalment_Amount_Base',
        'Regular_Monthly_Instalment_Amount_Retail', 'Regular_Monthly_Instalment_Amount_Base', 'Additional_Fees_Retail',
        'Additional_Fees_Base', 'Final_Payment_Retail', 'Final_Payment_Base','Mandatory_Dealer_Contribution_Retail', 'Mandatory_Dealer_Contribution_Base', 'Oem_Discount_Retail', 'Oem_Discount_Base',
        'Government_Contribution_Retail', 'Government_Contribution_Base', 'Downpayment_Allowance_Retail',
        'Downpayment_Allowance_Base', 'Captive_Rebate_Retail', 'Captive_Rebate_Base', 'Free_Supply_Amount',
        'Residual_Value_Retail', 'Residual_Value_Base','Excess_Mileage_Retail', 'Excess_Mileage_Base', 'Reimbursement_Mileage_Retail', 'Reimbursement_Mileage_Base',
        'Courtesy_Car_Amount', 'Supply_Amount', 'Cost_To_Terminate_The_Contract_Retail',
        'Cost_To_Terminate_The_Contract_Base', 'Road_Assistance_Amount', 'Tyres_Amount', 'Maintenance_Amount',
        'Repair_Amount', 'Service_Amount', 'Sourced_Financed_Amount_Retail', 'Sourced_Financed_Amount_Base'
    ]

    int_fields = [
        'Price', 'Contract_Duration_Months', 'Yearly_Mileage_Km', 'Yearly_Mileage_Miles',
        'Total_Contract_Mileage_Km', 'Total_Contract_Mileage_Miles', 'Deposit_Percentage_Of_Price',
        'Of_Monthly_Payments_In_Advance', 'Of_Monthly_Instalments', 'First_Monthly_Instalment_Amount_Retail',
        'First_Monthly_Instalment_Amount_Base', 'Regular_Monthly_Instalment_Amount_Retail',
        'Regular_Monthly_Instalment_Amount_Base', 'Additional_Fees_Retail', 'Additional_Fees_Base',
        'Final_Payment_Percentage_Of_Price', 'Mandatory_Dealer_Contribution_Percentage_Of_Price',
        'Oem_Discount_Percentage_Of_Price', 'Government_Contribution_Percentage_Of_Price',
        'Downpayment_Allowance_Percentage_Of_Price', 'Captive_Rebate_Percentage_Of_Price',
        'Free_Supply_Amount', 'Residual_Value_Percentage_Of_Price', 'Lease_Factor_Index', 'Excess_Mileage_Retail',
        'Excess_Mileage_Base', 'Reimbursement_Mileage_Retail', 'Reimbursement_Mileage_Base',
        'Courtesy_Car_Duration_Months', 'Courtesy_Car_Amount', 'Supply_Duration_Months', 'Supply_Amount',
        'Fuel_Quantity_L', 'Fuel_Quantity_Gal', 'Electricity_Quantity_Kw', 'Road_Assistance_Duration_Months',
        'Road_Assistance_Distance_Km', 'Road_Assistance_Distance_Miles', 'Road_Assistance_Amount',
        'Notice_To_Terminate_The_Contract_Mths', 'Cost_To_Terminate_Contract_Percentage_Of_Price',
        'Cost_To_Terminate_The_Contract_Retail', 'Cost_To_Terminate_The_Contract_Base', 'Of_Summer_Tyres',
        'Of_Winter_Tyres', 'Of_All_Seasons_Tyres', 'Tyres_Amount', 'Premium_Tyres', 'Tyres_Storage_Service',
        'Maintenance_Duration_Months', 'Maintenance_Distance_Km', 'Maintenance_Distance_Miles', 'Maintenance_Amount',
        'Repair_Duration_Months', 'Repair_Distance_Km', 'Repair_Distance_Miles', 'Repair_Amount',
        'Service_Duration_Months', 'Service_Distance_Km', 'Service_Distance_Miles', 'Service_Amount','Delivery_Costs_Retail',
        'Downpayment_Allowance_Retail','Deposit_Retail','Downpayment_Allowance_Base','Deposit_Base'
    ]

    calculable_fields = [
        'Price','Total_Contract_Mileage_Km', 'Total_Contract_Mileage_Miles','Yearly_Mileage_Km', 'Yearly_Mileage_Miles',
        'Deposit_Percentage_Of_Price','Final_Payment_Percentage_Of_Price','Mandatory_Dealer_Contribution_Percentage_Of_Price',
        'Oem_Discount_Percentage_Of_Price','Government_Contribution_Percentage_Of_Price','Downpayment_Allowance_Percentage_Of_Price',
    ]

    date_fields = [
        'Data_Date',
        'Conclude_Date',
        'Research_Date',
        'Start_Date',
        'End_Date',
        'Published_Start_Date',
        'Published_End_Date'
    ]