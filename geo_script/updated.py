import requests
import csv
import time

# Overpass API URL
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Define bounding boxes to cover the entire UK
UK_BOUNDING_BOXES = [
    # [50.0, -10.0, 51.0, -5.0],  # South West UK
    # [51.0, -10.0, 52.0, -5.0],  # Mid West UK
    # [52.0, -10.0, 53.0, -5.0],  # North West UK
    # [53.0, -10.0, 54.0, -5.0],  # Northern England/Scotland border
    # [50.0, -5.0, 51.0, 0.0],  # South East UK (London area)
    [51.0, -5.0, 52.0, 0.0],  # Mid East UK
    # [52.0, -5.0, 53.0, 0.0],  # North East UK
    # [53.0, -5.0, 54.0, 0.0],  # Northern England
]


# Function to create an Overpass query with bounding box
def create_overpass_query(bbox):
    min_lat, min_lon, max_lat, max_lon = bbox
    query = f"""
    [out:json][timeout:900];
    (
      way["highway"](around:100000, {min_lat},{min_lon},{max_lat},{max_lon});
    );
    out body;
    >;
    out skel qt;
    """
    return query


# Fetch data from Overpass API for a specific bounding box
def fetch_traffic_data(query):
    try:
        response = requests.post(OVERPASS_URL, data={'data': query})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


# Classify traffic based on maxspeed and lanes into red (high), yellow (moderate), green (low)
def classify_traffic(tags):
    maxspeed = tags.get('maxspeed', 'N/A')
    lanes = tags.get('lanes', 'N/A')

    if isinstance(maxspeed, str):
        maxspeed = maxspeed.lower()
        if 'km/h' in maxspeed or 'mph' in maxspeed:
            try:
                maxspeed_value = int(maxspeed.replace(' km/h', '').replace(' mph', '').strip())
                if maxspeed_value >= 70:
                    return 'Green', 'Low'
                elif 30 <= maxspeed_value < 70:
                    return 'Yellow', 'Moderate'
                elif maxspeed_value < 30:
                    return 'Red', 'High'
            except ValueError:
                return 'Unknown'

    if lanes != 'N/A' and isinstance(lanes, str):
        try:
            lanes_value = int(lanes)
            if lanes_value >= 4:
                return 'Red', 'High'
            elif 2 <= lanes_value < 4:
                return 'Yellow', 'Moderate'
            elif lanes_value == 1:
                return 'Green', 'Low'
        except ValueError:
            return 'Unknown'

    return 'Unknown'


# Save traffic data to a CSV file incrementally
def save_to_csv_incremental(data, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for element in data.get('elements', []):
            if element['type'] == 'way':
                tags = element.get('tags', {})
                traffic_level = classify_traffic(tags)

                location_name = tags.get('name', 'N/A')
                coords = 'N/A'

                if 'geometry' in element:
                    coords = "; ".join([f"{node['lat']},{node['lon']}" for node in element['geometry']])
                elif 'center' in element:
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
    for i, bbox in enumerate(UK_BOUNDING_BOXES):
        # Create a unique filename for each bounding box
        filename = f'new_uk_traffic_data_bbox_6.csv'

        # Open CSV and write headers once for each bounding box
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["ID", "Location Name", "Highway Type", "Max Speed", "Lanes", "Traffic Level (Color)", "Coordinates"])

        query = create_overpass_query(bbox)
        print(f"Fetching data for bounding box {bbox}...")

        data = fetch_traffic_data(query)
        if data:
            print(f"Fetched {len(data['elements'])} elements.")
            save_to_csv_incremental(data, filename)  # Save incrementally to a separate file
        else:
            print(f"No data fetched for bounding box {bbox}.")

        # Add a delay to avoid overwhelming the API
        # time.sleep(5)

    print("Traffic data saved for each bounding box.")
