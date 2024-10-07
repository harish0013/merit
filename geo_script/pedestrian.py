import requests
import csv

# Define the Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"
nominatim_url = "https://nominatim.openstreetmap.org/search"

# Define the Overpass API query
overpass_query = """
[out:json];
area[name="Islington"]->.searchArea;
way["highway"](area.searchArea);
out body;
>;
out skel qt;
"""


# Function to get full address using Nominatim
def get_full_address(street_name):
    params = {
        'q': street_name + ', Islington, UK',
        'format': 'json',
        'addressdetails': 1
    }
    response = requests.get(nominatim_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Make the request to the Overpass API
response = requests.get(overpass_url, params={'data': overpass_query})

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract street names, types, and addresses
    street_info = []
    for element in data['elements']:
        if 'tags' in element:
            street_name = element['tags'].get('name', 'Unnamed')
            street_type = element['tags'].get('highway', 'Unknown')

            # Get full address
            full_address = get_full_address(street_name)
            if full_address and len(full_address) > 0:
                address = full_address[0].get('display_name', 'Address not found')
            else:
                address = 'Address not found'

            street_info.append({'name': street_name, 'type': street_type, 'address': address})

    # Save street information to CSV
    csv_file = "islington_streets.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'type', 'address'])
        writer.writeheader()  # Write the header
        writer.writerows(street_info)  # Write the data rows

    print(f"Street information saved to {csv_file}")

else:
    print(f"Error: {response.status_code}")

