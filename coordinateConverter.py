import pandas as pd
import requests
import json
import argparse

#Command line argument. filename of CSV with data
parser = argparse.ArgumentParser(description="Convert US Feet Coordinates to WGS84")
parser.add_argument('filename',type=str,help="filename of CSV file with LA Parking Citation Data to be converted")
arg = parser.parse_args()

#Read CSV file containing US Feet Coordinates
data = pd.read_csv(arg.filename)
data.head()
lat = data['Latitude'].values
lon = data['Longitude'].values

#Create file to extract cordinates and put in proper format for API
filo = open('formattedCoords.txt', 'a+')
for la,lo in zip(lat,lon):
	filo.write(str(la)+','+str(lo)+';')
filo.close()

#API URL
http = str('http://epsg.io/trans?data=')
#Codes for conversion from US Feet Coordinates(102645) to World Geodetic System 1984(4326)
attr = str('&s_srs=102645&t_srs=4326')
with open("formattedCoords.txt", "r") as file:
	coords = file.read()
file.close()

#Making HTTP Request to the API
url = http + coords + attr
#Remove extra semicolon at the end of the coords
url = url.replace(';&s_srs', '&s_srs')
page = requests.get(url)
content = page.content
print url
print "Response Code: " + str(page.status_code)

resData = json.loads(content)
lats = []
lons = []
for d in resData:
	lats.append(d.get("y"))
	lons.append(d.get("x"))


dic = {'lat':lats,'lon':lons}
df = pd.DataFrame(dic)

data['Latitude'] = df['lat']
data['Longitude'] = df['lon']
print data.head(5)
vital_columns = ["Ticket number","Issue Date","Issue time","Make","Body Style","Color","Location","Violation code","Violation Description","Fine amount","Latitude","Longitude"]
data.to_csv("Parking_Citations_sample_trans.csv",columns=vital_columns,header=vital_columns,index=False)