import requests
import csv


# Function to fetch green groceries from Overpass API
def fetch_green_groceries():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area["name"="United Kingdom"]->.searchArea;
    (
      node["shop"="greengrocer"](area.searchArea);
      way["shop"="greengrocer"](area.searchArea);
      relation["shop"="greengrocer"](area.searchArea);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        return response.json().get('elements', [])
    else:
        print(f"Error fetching groceries: {response.status_code}")
        return []


# Function to fetch nearby restaurants from Overpass API
def fetch_nearby_restaurants(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="restaurant"](around:500, {lat}, {lon});
      way["amenity"="restaurant"](around:500, {lat}, {lon});
      relation["amenity"="restaurant"](around:500, {lat}, {lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        return response.json().get('elements', [])
    else:
        print(f"Error fetching restaurants: {response.status_code}")
        return []


# Function to fetch nearby schools from Overpass API
def fetch_nearby_schools(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="school"](around:500, {lat}, {lon});
      way["amenity"="school"](around:500, {lat}, {lon});
      relation["amenity"="school"](around:500, {lat}, {lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        return response.json().get('elements', [])
    else:
        print(f"Error fetching schools: {response.status_code}")
        return []


# Function to reverse geocode (get address from latitude and longitude)
def reverse_geocode(lat, lon):
    reverse_geocode_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(reverse_geocode_url)

    if response.status_code == 200:
        return response.json().get('display_name', 'Unknown address')
    else:
        print(f"Error fetching address: {response.status_code}")
        return 'Unknown address'


# Function to check for pedestrian accessibility
def fetch_accessibility(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      way["highway"~"footway|path|pedestrian"](around:500, {lat}, {lon});
      node["highway"~"footway|path|pedestrian"](around:500, {lat}, {lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        elements = response.json().get('elements', [])
        return len(elements) > 0  # Returns True if there are accessible paths
    else:
        print(f"Error fetching accessibility: {response.status_code}")
        return False


# Function to check for roadblocks
def fetch_roadblocks(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["barrier"="block"](around:500, {lat}, {lon});
      way["barrier"="block"](around:500, {lat}, {lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        elements = response.json().get('elements', [])
        return len(elements) > 0  # Returns True if there are roadblocks
    else:
        print(f"Error fetching roadblocks: {response.status_code}")
        return False


# Function to check for pedestrian crossings
def fetch_pedestrian_crossings(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["highway"="crossing"](around:500, {lat}, {lon});
      way["highway"="crossing"](around:500, {lat}, {lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        elements = response.json().get('elements', [])
        return len(elements) > 0  # Returns True if pedestrian crossings exist
    else:
        print(f"Error fetching pedestrian crossings: {response.status_code}")
        return False


# Main function to combine data and save to CSV
def main():
    # Fetch green groceries
    green_groceries = fetch_green_groceries()

    # Prepare CSV file to save the data
    with open('green_groceries_restaurants_schools_accessibility_roadblocks_crossings.csv', mode='w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write CSV header
        writer.writerow(
            ['Grocery Name', 'Grocery Latitude', 'Grocery Longitude', 'Grocery Address', 'Nearby Restaurant',
             'Restaurant Latitude', 'Restaurant Longitude', 'Restaurant Address', 'Nearby School', 'School Latitude',
             'School Longitude', 'School Address', 'Accessibility', 'Roadblocks', 'Pedestrian Crossings'])

        if green_groceries:
            print(f"Found {len(green_groceries)} green grocery stores in the UK. Saving to CSV...")
            for grocery in green_groceries:
                grocery_lat = grocery.get('lat')
                grocery_lon = grocery.get('lon')
                grocery_name = grocery.get('tags', {}).get('name', 'Unnamed')
                grocery_address = reverse_geocode(grocery_lat, grocery_lon)  # Fetch grocery address

                # Fetch nearby restaurants
                nearby_restaurants = fetch_nearby_restaurants(grocery_lat, grocery_lon)

                if nearby_restaurants:
                    for restaurant in nearby_restaurants:
                        restaurant_name = restaurant.get('tags', {}).get('name', 'Unnamed')
                        restaurant_lat = restaurant.get('lat', 'Unknown')
                        restaurant_lon = restaurant.get('lon', 'Unknown')
                        restaurant_address = reverse_geocode(restaurant_lat, restaurant_lon)  # Fetch restaurant address

                        # Fetch nearby schools
                        nearby_schools = fetch_nearby_schools(restaurant_lat, restaurant_lon)

                        if nearby_schools:
                            for school in nearby_schools:
                                school_name = school.get('tags', {}).get('name', 'Unnamed')
                                school_lat = school.get('lat', 'Unknown')
                                school_lon = school.get('lon', 'Unknown')
                                school_address = reverse_geocode(school_lat, school_lon)  # Fetch school address

                                # Check for pedestrian accessibility
                                accessibility = fetch_accessibility(restaurant_lat, restaurant_lon)

                                # Check for roadblocks
                                roadblocks = fetch_roadblocks(restaurant_lat, restaurant_lon)

                                # Check for pedestrian crossings
                                crossings = fetch_pedestrian_crossings(restaurant_lat, restaurant_lon)

                                # Write grocery, restaurant, school, and additional data to CSV
                                writer.writerow(
                                    [grocery_name, grocery_lat, grocery_lon, grocery_address, restaurant_name,
                                     restaurant_lat, restaurant_lon, restaurant_address, school_name, school_lat,
                                     school_lon, school_address,
                                     'Yes' if accessibility else 'No', 'Yes' if roadblocks else 'No',
                                     'Yes' if crossings else 'No'])
                        else:
                            # If no schools found, still write grocery and restaurant details
                            accessibility = fetch_accessibility(restaurant_lat, restaurant_lon)
                            roadblocks = fetch_roadblocks(restaurant_lat, restaurant_lon)
                            crossings = fetch_pedestrian_crossings(restaurant_lat, restaurant_lon)
                            writer.writerow([grocery_name, grocery_lat, grocery_lon, grocery_address, restaurant_name,
                                             restaurant_lat, restaurant_lon, restaurant_address, 'No nearby schools', '',
                                             '', 'No address', 'Yes' if accessibility else 'No',
                                             'Yes' if roadblocks else 'No', 'Yes' if crossings else 'No'])
                else:
                    # If no restaurants found, still write the grocery details
                    writer.writerow(
                        [grocery_name, grocery_lat, grocery_lon, grocery_address, 'No nearby restaurants', '', '', '',
                         'No nearby schools', '', '', 'No address', 'No', 'No', 'No'])

        print("Data saved to CSV file.")

# Run the main function
if __name__ == "__main__":
    main()
