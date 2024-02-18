# calculate distance between two points given their latitudes and longitudes
import haversine as hs
from haversine import Unit

# given two locations
def distance(loc1, loc2):
    '''
    get distance between points given latitudes and longitudes
    '''
    result = hs.haversine(loc1, loc2, unit=Unit.KILOMETERS)
    return result

if __name__ == "__main__":
    loc1 = tuple(map(float, input("Enter latitude and longitude for location 1, separated by a space: ").split()))
    loc2 = tuple(map(float, input("Enter latitude and longitude for location 2, separated by a space: ").split()))
    print("The distance calculated is: " + str(distance(loc1, loc2)) + " kilometers.")
