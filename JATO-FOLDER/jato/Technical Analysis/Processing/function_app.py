import azure.functions as func
import logging
from Data_processing.data_cleaning import clean_data
from Data_processing.data_transformation import transform_data
from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import date
import json

app = func.FunctionApp()

@app.function_name(name="data_processing_trigger")
@app.blob_trigger(arg_name="myblob", path="rawdata/{name}",connection="AzureWebJobsStorage") 
def blob_trigger_dp(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    try:
    
        json_data = myblob.read()
        json_data = json.loads(json_data)
        
        # Convert JSON data to DataFrame
        df = pd.DataFrame(json_data)

        # Perform data cleaning
        df = clean_data(df)

        # Perform data transformation
        df = transform_data(df)

        # Get the current date to create a folder
        current_date = date.today()
        folder_name = f"processed_on_{current_date}"

        # Use the original name of the blob
        original_blob_name = myblob.name.split('/')[-1]  # Extracts the original file name, e.g., "example.json"
        original_blob_name = original_blob_name.replace('scraper_raw','processed')

        # Create a new blob name with the folder structure and original name
        blob_name = f"{folder_name}/{original_blob_name}"

        processed_json = df.to_json(orient='records')

        # Save the processed data back to the processeddata container
        processed_blob_client = BlobServiceClient.from_connection_string(
            "DefaultEndpointsProtocol=https;AccountName=jatoproject;AccountKey=Ih93978inR59FMdrMgZk1kHCNFwpMFQkZrbYYfVIujHG7lIjkwB/ysLJgldgLi2mpd+rzOz6W8dX+ASt6r0+nA==;EndpointSuffix=core.windows.net"
        ).get_blob_client(container="processeddata", blob=blob_name)

        logging.info(f"Uploading data for {blob_name}.")

        processed_blob_client.upload_blob(processed_json, overwrite=True)

        logging.info(f"Processed data for {blob_name} stored successfully.")

    except Exception as e:
        logging.error(f"Error processing blob {myblob.name}: {str(e)}")