import argparse
import math

#Command line argument. filename of CSV with data
parser = argparse.ArgumentParser(description="Get distance (Km) between two WGS84 Coodrinates")
parser.add_argument('lat1',type=float,help="la1")
parser.add_argument('lon1',type=float,help="lo1")
parser.add_argument('lat2',type=float,help="la2")
parser.add_argument('lon2',type=float,help="lo2")
arg = parser.parse_args()

earth_rad = 6371 #km
dLat = math.radians(arg.lat2-arg.lat1)
dLon = math.radians(arg.lon2-arg.lon1)
a = math.sin(dLat/2)**2 + math.cos(math.radians(arg.lat1)) * math.cos(math.radians(arg.lat2)) * math.sin(dLon/2)**2
c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
d = earth_rad * c
print d