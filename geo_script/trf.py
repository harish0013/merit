import requests
import csv
import reverse_geocoder as rg
from multiprocessing import Pool, freeze_support
import gc
import time

# Define the Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Overpass Query for Low Traffic and High Traffic Features in the UK
overpass_query = """
[out:json];
area["name"="United Kingdom"]->.uk;

(
  node(area.uk)["traffic_calming"];
  way(area.uk)["traffic_calming"];
  relation(area.uk)["traffic_calming"];

  node(area.uk)["barrier"~"bollard|gate|block"];
  way(area.uk)["barrier"~"bollard|gate|block"];

  way(area.uk)["motor_vehicle"="no"];
  way(area.uk)["access"="no"];

  way(area.uk)["cycleway"="track"];
  way(area.uk)["footway"];

  way(area.uk)["highway"~"primary|secondary|tertiary"];
  node(area.uk)["highway"~"primary|secondary|tertiary"];
);

out body;
>;
out skel qt;
"""

# Function to get location name from latitude and longitude
def get_location_name(coordinates):
    try:
        result = rg.search([coordinates])
        return result[0]['name'], result[0]['admin1'], result[0]['cc']  # City, region, country code
    except Exception as e:
        print(f"Geocoding error: {e}")
        return "Unknown", "Unknown", "Unknown"

# Function to process each element and prepare data
def process_element(element):
    el_type = element['type']
    el_id = element['id']
    el_tags = element.get('tags', {})
    is_ltn = "traffic_calming" in el_tags or "barrier" in el_tags or el_tags.get("motor_vehicle") == "no"
    is_high_traffic = "highway" in el_tags  # Identify if it's a high traffic area

    latitude, longitude = 'NA', 'NA'
    location_name = "Unknown"

    if el_type == 'node':
        latitude = element['lat']
        longitude = element['lon']
        return [el_id, el_type, latitude, longitude, location_name, el_tags, is_ltn, is_high_traffic]

    return [el_id, el_type, latitude, longitude, location_name, el_tags, is_ltn, is_high_traffic]

# Send the request to Overpass API
response = requests.get(overpass_url, params={'data': overpass_query})

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
else:
    print(f"Error: {response.status_code}")
    exit()

# Prepare to process elements with multiprocessing
elements = data['elements']

# Initialize csv_data before processing
csv_data = []

# Use multiprocessing to handle the initial processing
if __name__ == '__main__':
    freeze_support()  # For Windows support
    with open('traffic_neighbourhoods_uk.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Type', 'Latitude', 'Longitude', 'Location Name', 'Tags', 'Is LTN', 'Is High Traffic'])

        with Pool(processes=2) as pool:  # Reduce the number of processes
            try:
                # Process elements in smaller chunks
                for chunk in (elements[i:i + 1000] for i in range(0, len(elements), 1000)):
                    partial_data = pool.map(process_element, chunk)

                    # Retrieve location names in the main process
                    for i, element in enumerate(partial_data):
                        if element[2] != 'NA':  # Check if latitude is valid
                            location_name, region, country = get_location_name((element[2], element[3]))
                            element[4] = location_name  # Update location name

                        # Write each row to CSV immediately after processing
                        writer.writerow(element)
                        csv_file.flush()  # Ensure data is written immediately

                    csv_data.extend(partial_data)
                    gc.collect()  # Force garbage collection after processing each chunk
            except Exception as e:
                print(f"Error during processing: {e}")
                exit()

print("Data saved to traffic_neighbourhoods_uk.csv")
