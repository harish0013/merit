import requests
import csv
import time

# Define the Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"
nominatim_url = "https://nominatim.openstreetmap.org/search"

# Define the Overpass API query for Gloucester
overpass_query = """
[out:json];
area[name="Gloucester"]->.searchArea;
way["highway"](area.searchArea);
out body;
>;
out skel qt;
"""


# Function to get full address using Nominatim
def get_full_address(street_name):
    params = {
        'q': f"{street_name}, Gloucester, UK",
        'format': 'json',
        'addressdetails': 1
    }
    response = requests.get(nominatim_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Function to fetch street names and types from the Overpass API
def fetch_streets():
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        data = response.json()

        # Extract street names, types, and addresses
        street_info = []
        for element in data['elements']:
            if 'tags' in element:
                street_name = element['tags'].get('name', 'Unnamed')  # Get name
                street_type = element['tags'].get('highway', 'Unknown')  # Get type

                # Get full address
                full_address_data = get_full_address(street_name)
                if full_address_data and len(full_address_data) > 0:
                    address = full_address_data[0].get('display_name', 'Address not found')
                else:
                    address = 'Address not found'

                # Append street information to the list
                street_info.append({
                    'name': street_name,
                    'type': street_type,
                    'address': address
                })

                # Optional: Add a delay to respect Nominatim's usage policy
                # time.sleep(1)  # Add a delay of 1 second

        return street_info
    else:
        print(f"Error: {response.status_code}")
        return []


# Function to save street information to a CSV file
def save_to_csv(street_info, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'type', 'address'])
        writer.writeheader()  # Write the header
        writer.writerows(street_info)  # Write the data rows


# Main script execution
if __name__ == "__main__":
    streets = fetch_streets()
    if streets:
        save_to_csv(streets, "gloucester_streets_with_addresses.csv")
        print("Street information with addresses saved to gloucester_streets_with_addresses.csv")
    else:
        print("No street information retrieved.")
