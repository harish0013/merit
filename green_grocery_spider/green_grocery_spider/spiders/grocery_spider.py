import scrapy
import json
import csv
import urllib.parse

class GrocerySpider(scrapy.Spider):
    name = "grocery_spider"
    allowed_domains = ["overpass-api.de"]

    def start_requests(self):
        # Define the query for green grocers in the UK
        query = """
        [out:json];
        (
          node[shop='greengrocer'](51.0,-5.0,59.0,1.0);
        );
        out center;
        """
        encoded_query = urllib.parse.quote(query)
        url = f"http://overpass-api.de/api/interpreter?data={encoded_query}"
        yield scrapy.Request(url, callback=self.parse_groceries)

    def parse_groceries(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to fetch data: {response.status} - {response.text}")
            return

        groceries = json.loads(response.text).get('elements', [])
        if not groceries:
            self.logger.warning("No green groceries found.")
            return

        for grocery in groceries:
            grocery_name = grocery.get('tags', {}).get('name', 'Unnamed')
            grocery_lat = grocery.get('lat')
            grocery_lon = grocery.get('lon')

            # Fetch nearby restaurants
            restaurants_url = f"http://overpass-api.de/api/interpreter?data=[out:json];(node[amenity='restaurant'](around:500,{grocery_lat},{grocery_lon});out center;);"
            yield scrapy.Request(restaurants_url, callback=self.parse_restaurants,
                                 meta={'grocery_name': grocery_name, 'grocery_lat': grocery_lat, 'grocery_lon': grocery_lon})

    def parse_restaurants(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to fetch restaurants: {response.status} - {response.text}")
            return

        grocery_name = response.meta['grocery_name']
        grocery_lat = response.meta['grocery_lat']
        grocery_lon = response.meta['grocery_lon']
        restaurants = json.loads(response.text).get('elements', [])

        for restaurant in restaurants:
            restaurant_name = restaurant.get('tags', {}).get('name', 'Unnamed')
            restaurant_lat = restaurant.get('lat')
            restaurant_lon = restaurant.get('lon')

            # Fetch nearby schools
            schools_url = f"http://overpass-api.de/api/interpreter?data=[out:json];(node[amenity='school'](around:500,{restaurant_lat},{restaurant_lon});out center;);"
            yield scrapy.Request(schools_url, callback=self.parse_schools,
                                 meta={'grocery_name': grocery_name, 'grocery_lat': grocery_lat,
                                       'grocery_lon': grocery_lon, 'restaurant_name': restaurant_name,
                                       'restaurant_lat': restaurant_lat, 'restaurant_lon': restaurant_lon})

    def parse_schools(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to fetch schools: {response.status} - {response.text}")
            return

        grocery_name = response.meta['grocery_name']
        grocery_lat = response.meta['grocery_lat']
        grocery_lon = response.meta['grocery_lon']
        restaurant_name = response.meta['restaurant_name']
        restaurant_lat = response.meta['restaurant_lat']
        restaurant_lon = response.meta['restaurant_lon']

        schools = json.loads(response.text).get('elements', [])
        for school in schools:
            school_name = school.get('tags', {}).get('name', 'Unnamed')
            school_lat = school.get('lat')
            school_lon = school.get('lon')

            # Check for pedestrian accessibility
            accessibility_url = f"http://overpass-api.de/api/interpreter?data=[out:json];(way[highway~'footway|path|pedestrian'](around:500,{restaurant_lat},{restaurant_lon});out center;);"
            yield scrapy.Request(accessibility_url, callback=self.check_accessibility,
                                 meta={'grocery_name': grocery_name, 'grocery_lat': grocery_lat,
                                       'grocery_lon': grocery_lon, 'restaurant_name': restaurant_name,
                                       'restaurant_lat': restaurant_lat, 'restaurant_lon': restaurant_lon,
                                       'school_name': school_name, 'school_lat': school_lat,
                                       'school_lon': school_lon})

    def check_accessibility(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to check accessibility: {response.status} - {response.text}")
            return

        grocery_name = response.meta['grocery_name']
        grocery_lat = response.meta['grocery_lat']
        grocery_lon = response.meta['grocery_lon']
        restaurant_name = response.meta['restaurant_name']
        restaurant_lat = response.meta['restaurant_lat']
        restaurant_lon = response.meta['restaurant_lon']
        school_name = response.meta['school_name']
        school_lat = response.meta['school_lat']
        school_lon = response.meta['school_lon']

        elements = json.loads(response.text).get('elements', [])
        accessibility = 'Yes' if len(elements) > 0 else 'No'

        # Write data to CSV
        with open('green_groceries_restaurants_schools_accessibility_uk.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([grocery_name, grocery_lat, grocery_lon, restaurant_name, restaurant_lat,
                             restaurant_lon, school_name, school_lat, school_lon, accessibility])
