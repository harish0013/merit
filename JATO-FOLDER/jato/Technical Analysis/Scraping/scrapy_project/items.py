# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class VehicleItem(scrapy.Item):

    # Vehicle Information
    Make = scrapy.Field()
    Model = scrapy.Field()
    Trim = scrapy.Field()
    Derivative = scrapy.Field()
    Derivative_Translated_English = scrapy.Field()
    Number_Of_Doors = scrapy.Field()
    Body_Type = scrapy.Field()
    Power_Train = scrapy.Field()
    Version_Name = scrapy.Field()
    Version_Name_Translated_English = scrapy.Field()
    Manufacturer_S_Code = scrapy.Field()
    Configurator_Model_Year = scrapy.Field()
    Built_Option_Pack = scrapy.Field()
    Uid = scrapy.Field()
    Data_Date = scrapy.Field()
    Conclude_Date = scrapy.Field()
    Version_Availability = scrapy.Field()
    
    # Pricing and Costs
    Currency = scrapy.Field()
    Price = scrapy.Field()
    Delivery_Costs_Retail = scrapy.Field()
    Cost_To_Return_The_Vehicle_Retail = scrapy.Field()
    Total_Mandatory_Packs_Amount = scrapy.Field()
    
    # Dates
    Country = scrapy.Field()
    Research_Date = scrapy.Field()
    Start_Date = scrapy.Field()
    End_Date = scrapy.Field()
    
    # Customer and Payment Information
    Customer_Type = scrapy.Field()
    Monthly_Payment_Type = scrapy.Field()
    Product_Name = scrapy.Field()
    Product_Description = scrapy.Field()
    Monthly_Payment_Provider_Name = scrapy.Field()
    Monthly_Payment_Provider_Type = scrapy.Field()
    Interest_Rate_Apr = scrapy.Field()
    Interest_Rate_Nominal = scrapy.Field()
    Contract_Duration_Months = scrapy.Field()
    Yearly_Mileage_Km = scrapy.Field()
    Yearly_Mileage_Miles = scrapy.Field()
    Total_Contract_Mileage_Km = scrapy.Field()
    Total_Contract_Mileage_Miles = scrapy.Field()
    Deposit_Percentage_Of_Price = scrapy.Field()
    Deposit_Retail = scrapy.Field()
    Deposit_Base = scrapy.Field()
    Final_Payment_Base = scrapy.Field()

    Of_Monthly_Payments_In_Advance = scrapy.Field()
    Of_Monthly_Instalments = scrapy.Field()
    First_Monthly_Instalment_Amount_Retail = scrapy.Field()
    First_Monthly_Instalment_Amount_Base = scrapy.Field()
    Regular_Monthly_Instalment_Amount_Retail = scrapy.Field()
    Regular_Monthly_Instalment_Amount_Base = scrapy.Field()
    Additional_Fees_Retail = scrapy.Field()
    Additional_Fees_Base = scrapy.Field()
    Final_Payment_Type = scrapy.Field()
    Final_Payment_Percentage_Of_Price = scrapy.Field()
    Final_Payment_Retail = scrapy.Field()
    

    # Data Sources
    Data_Source = scrapy.Field()
    Web_Source_Url = scrapy.Field()
    
    # Advertised Pricing and Published Dates
    Advertised_Price_Point_Monthly_Payment = scrapy.Field()
    Published_Start_Date = scrapy.Field()
    Published_End_Date = scrapy.Field()
    
    # Financial Configurators
    Oem_Web_Financial_Configurator_Source = scrapy.Field()
    Captive_Financial_Configurator_Source = scrapy.Field()
    Non_Captive_Financial_Configurator_Source = scrapy.Field()
    Bank_Financial_Configurator_Source = scrapy.Field()
    
    # Sourced Quotes and Sources
    Sourced_Dealer_Quote = scrapy.Field()
    Jato_Internal_Source = scrapy.Field()
    Other_Sources = scrapy.Field()
    
    # Vehicle Price Reference
    Vehicle_Price_Reference = scrapy.Field()
    
    # Dealer Contributions and Discounts
    Mandatory_Dealer_Contribution_Percentage_Of_Price = scrapy.Field()
    Mandatory_Dealer_Contribution_Retail = scrapy.Field()
    Mandatory_Dealer_Contribution_Base = scrapy.Field()
    Oem_Discount_Percentage_Of_Price = scrapy.Field()
    Oem_Discount_Retail = scrapy.Field()
    Oem_Discount_Base = scrapy.Field()
    Government_Contribution_Percentage_Of_Price = scrapy.Field()
    Government_Contribution_Retail = scrapy.Field()
    Government_Contribution_Base = scrapy.Field()
    
    # Downpayment Allowance and Rebate
    Downpayment_Allowance_Percentage_Of_Price = scrapy.Field()
    Downpayment_Allowance_Retail = scrapy.Field()
    Downpayment_Allowance_Base = scrapy.Field()
    Captive_Rebate_Percentage_Of_Price = scrapy.Field()
    Captive_Rebate_Retail = scrapy.Field()
    Captive_Rebate_Base = scrapy.Field()
    
    # Financial Configurator Sources
    Free_Supply_Amount = scrapy.Field()
    Residual_Value_Percentage_Of_Price = scrapy.Field()
    Residual_Value_Retail = scrapy.Field()
    Residual_Value_Base = scrapy.Field()
    Lease_Factor_Index = scrapy.Field()
    
    # Insurance and Supply
    Insurance = scrapy.Field()
    Theft_And_Fire_Insurance = scrapy.Field()
    Insurance_Description = scrapy.Field()
    Sourced_Financed_Amount_Percentage_Of_Price = scrapy.Field()
    Sourced_Financed_Amount_Retail = scrapy.Field()
    Sourced_Financed_Amount_Base = scrapy.Field()
    
    # Unique Identifiers and Status
    Unique_Id = scrapy.Field()
    Change_Status = scrapy.Field()
    Updates_Column = scrapy.Field()
    Back_End_Data = scrapy.Field()
    Vehicle_Hash = scrapy.Field()
    
    # Mileage and Costs
    Excess_Mileage_Retail = scrapy.Field()
    Excess_Mileage_Base = scrapy.Field()
    Reimbursement_Mileage_Retail = scrapy.Field()
    Reimbursement_Mileage_Base = scrapy.Field()
    
    # Courtesy Car
    Courtesy_Car = scrapy.Field()
    Courtesy_Car_Description = scrapy.Field()
    Courtesy_Car_Duration_Months = scrapy.Field()
    Courtesy_Car_Amount = scrapy.Field()
    
    # Fuel and Electric Supply
    Fuel_And_Electric_Supply = scrapy.Field()
    Fuel_And_Electric_Supply_Description = scrapy.Field()
    Supply_Duration_Months = scrapy.Field()
    Supply_Amount = scrapy.Field()
    Fuel_Quantity_L = scrapy.Field()
    Fuel_Quantity_Gal = scrapy.Field()
    Electricity_Quantity_Kw = scrapy.Field()
    
    # Road Assistance
    Road_Assistance = scrapy.Field()
    Road_Assistance_Description = scrapy.Field()
    Road_Assistance_Duration_Months = scrapy.Field()
    Road_Assistance_Distance_Km = scrapy.Field()
    Road_Assistance_Distance_Miles = scrapy.Field()
    Road_Assistance_Amount = scrapy.Field()
    
    # Cancellation and Termination Costs
    Flexible_Early_Cancellation_Possible = scrapy.Field()
    Notice_To_Terminate_The_Contract_Mths = scrapy.Field()
    Cost_To_Terminate_Contract_Percentage_Of_Price = scrapy.Field()
    Cost_To_Terminate_The_Contract_Retail = scrapy.Field()
    Cost_To_Terminate_The_Contract_Base = scrapy.Field()
    Cost_To_Terminate_The_Contract_Description = scrapy.Field()
    
    # Tax and Tyres
    Road_Tax = scrapy.Field()
    Tyres = scrapy.Field()
    Tyres_Description = scrapy.Field()
    Tyres_Duration_Months = scrapy.Field()
    Of_Summer_Tyres = scrapy.Field()
    Of_Winter_Tyres = scrapy.Field()
    Of_All_Seasons_Tyres = scrapy.Field()
    Tyres_Amount = scrapy.Field()
    Premium_Tyres = scrapy.Field()
    Tyres_Storage_Service = scrapy.Field()
    
    # Maintenance and Repair
    Maintenance = scrapy.Field()
    Maintenance_Description = scrapy.Field()
    Maintenance_Duration_Months = scrapy.Field()
    Maintenance_Distance_Km = scrapy.Field()
    Maintenance_Distance_Miles = scrapy.Field()
    Maintenance_Amount = scrapy.Field()
    
    Repair = scrapy.Field()
    Repair_Description = scrapy.Field()
    Repair_Duration_Months = scrapy.Field()
    Repair_Distance_Km = scrapy.Field()
    Repair_Distance_Miles = scrapy.Field()
    Repair_Amount = scrapy.Field()
    
    # Service
    Service = scrapy.Field()
    Service_Description = scrapy.Field()
    Service_Duration_Months = scrapy.Field()
    Service_Distance_Km = scrapy.Field()
    Service_Distance_Miles = scrapy.Field()
    Service_Amount = scrapy.Field()