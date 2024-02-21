from haversine import haversine
import numpy as np
import pandas as pd
import osmnx as ox
from shapely.geometry import Point
from geopy.distance import great_circle
pd.set_option('display.max_columns', None)

superset_amenities = ['parking', 'restaurant', 'fire_station', 'cinema', 'dentist',
       'school', 'atm', 'fuel', 'fast_food', 'toilets', 'pharmacy',
       'bank', 'police', 'post_box', 'place_of_worship', 'bar', 'pub',
       'cafe', 'clinic', 'hospital', 'community_centre',
       'vending_machine', 'bus_station', 'health_post', 'college',
       'theatre', 'showroom', 'marketplace']

class AmenityDistanceCalculator:
    def __init__(self, lat, lon, radius):
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.center_point = (lat, lon)
        self.amenities = self.get_amenities()

    def haversine_distance(self, coord1, coord2):
        return great_circle(coord1, coord2).meters

    def get_amenities(self):
        # Get amenities
        amenities = ox.geometries_from_point(center_point=self.center_point, tags={"amenity": True}, dist=self.radius)

        # Drop unnecessary columns
        amenities = amenities[['amenity', 'geometry']]
        
        # Unpack 'geometry' into 'latitude' and 'longitude'
        amenities['latitude'] = amenities['geometry'].apply(lambda geom: geom.y if isinstance(geom, Point) else geom.centroid.y)
        amenities['longitude'] = amenities['geometry'].apply(lambda geom: geom.x if isinstance(geom, Point) else geom.centroid.x)

        # drop 'geometry' column
        amenities.drop('geometry', axis=1, inplace=True)

        # Rename 'amenity' column to 'Amenity'
        amenities.rename(columns={'amenity': 'Amenity'}, inplace=True)

        return amenities

    def calculate_distances(self, point):

        # Create a new DataFrame
        df_new = self.amenities.copy()

        # Calculate distances and convert to meters
        df_new['Amenity_distance_From_point'] = df_new.apply(lambda row: haversine(point, (row['latitude'], row['longitude'])) * 1000, axis=1)

        # Group by amenity and calculate sum of distances
        result = df_new.groupby('Amenity')['Amenity_distance_From_point'].sum().reset_index()
        return result

if __name__ == "__main__":
    # Define the point
    point = (17.442109, 78.498555)
    
    # make instance
    amenities_secunderabad = AmenityDistanceCalculator(lat=17.442109, lon= 78.498555,radius=2000)

    # Calculate distances
    result = amenities_secunderabad.calculate_distances(point)
    print(result)