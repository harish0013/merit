import requests
import csv

# Overpass API URL
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Overpass query for major highways in the UK
OVERPASS_QUERY = """
[out:json];
area["ISO3166-1"="GB"][admin_level=2];
(
  way["highway"~"motorway|trunk|primary"](area);
);
out body;
>;
out skel qt;
"""


# Fetch data from the Overpass API
def fetch_traffic_data(query):
    try:
        response = requests.post(OVERPASS_URL, data={'data': query})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


# Classify traffic based on maxspeed and lanes
def classify_traffic(tags):
    maxspeed = tags.get('maxspeed', 'N/A')
    lanes = tags.get('lanes', 'N/A')

    # Handle maxspeed properly
    if isinstance(maxspeed, str):
        maxspeed = maxspeed.lower()  # Normalize to lower case
        if 'km/h' in maxspeed:
            try:
                maxspeed_value = int(maxspeed.replace(' km/h', '').strip())
                if maxspeed_value >= 70:
                    return 'High Traffic'
                elif maxspeed_value < 30:
                    return 'Low Traffic'
            except ValueError:
                return 'Unknown Traffic'  # If conversion fails, return unknown

        elif 'mph' in maxspeed:
            try:
                maxspeed_value = int(maxspeed.replace(' mph', '').strip())
                if maxspeed_value >= 70:
                    return 'High Traffic'
                elif maxspeed_value < 30:
                    return 'Low Traffic'
            except ValueError:
                return 'Unknown Traffic'  # If conversion fails, return unknown

    # Handle lanes
    if lanes != 'N/A' and isinstance(lanes, str):  # Ensure lanes is a string before converting
        try:
            lanes_value = int(lanes)
            if lanes_value >= 4:
                return 'High Traffic'
            elif lanes_value == 1:
                return 'Low Traffic'
        except ValueError:
            return 'Unknown Traffic'  # If conversion fails, return unknown

    return 'Moderate Traffic'  # Default classification if no specific conditions are met


# Save traffic data to a CSV file
def save_to_csv(data, filename='uk_traffic_data.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Location Name", "Highway Type", "Max Speed", "Lanes", "Traffic Level", "Coordinates"])

        for element in data.get('elements', []):
            if element['type'] == 'way':
                tags = element.get('tags', {})
                traffic_level = classify_traffic(tags)

                location_name = tags.get('name', 'N/A')

                # Ensure we correctly handle missing or incomplete geometry data
                coords = 'N/A'
                if 'geometry' in element:
                    coords = "; ".join([f"{node['lat']},{node['lon']}" for node in element['geometry']])
                elif 'center' in element:
                    # Fallback to center if geometry isn't available
                    coords = f"{element['center']['lat']},{element['center']['lon']}"

                writer.writerow([
                    element['id'],
                    location_name,
                    tags.get('highway', 'N/A'),
                    tags.get('maxspeed', 'N/A'),
                    tags.get('lanes', 'N/A'),
                    traffic_level,
                    coords
                ])


# Main execution flow
if __name__ == "__main__":
    traffic_data = fetch_traffic_data(OVERPASS_QUERY)

    if traffic_data:
        print(f"Fetched {len(traffic_data['elements'])} elements from Overpass API.")
        save_to_csv(traffic_data)
        print("Traffic data saved to uk_traffic_data.csv")
    else:
        print("No data to save.")
