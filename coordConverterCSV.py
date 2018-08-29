import pandas as pd
import requests
import json
import argparse
from os import remove

#Next Steps: To convert more than 200 coordinates at a time use for loops and create more calls to the API
#Make the zip() into a list(zip()) then iterate over 200 coords at a time

# Add filename of CSV with data as a command line argument
parser = argparse.ArgumentParser(description="Convert US Feet Coordinates to WGS84")
parser.add_argument('filename',type=str,help="filename of CSV file with LA Parking Citation Data to be converted")
arg = parser.parse_args()

#Read CSV file containing US Feet Coordinates
data = pd.read_csv(arg.filename)
data.head()
lat = data['Latitude'].values
lon = data['Longitude'].values

#Create file to store cordinates in proper format for REST API HTTP Request
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
remove('formattedCoords.txt')

#Making HTTP Request to the API
url = http + coords + attr
#Removes extra semicolon at the end of the coords
url = url.replace(';&s_srs', '&s_srs')
page = requests.get(url)
content = page.content
print "Response Code: " + str(page.status_code)

#Grab the HTTP response and format to JSON
resData = json.loads(content)
lats = []
lons = []
for d in resData:
	lats.append(d.get("y"))
	lons.append(d.get("x"))

#Create a dictionary from the converted lats and longs
dic = {'lat':lats,'lon':lons}
df = pd.DataFrame(dic)

#Replace coordinates with new converted coordinates
data['Latitude'] = df['lat']
data['Longitude'] = df['lon']

#Specify which columns of the data to keep and save to csv file
vital_columns = ["Ticket number","Issue Date","Issue time","Make","Body Style","Color","Location","Violation code","Violation Description","Fine amount","Latitude","Longitude"]
convertedFile = "translated_"+arg.filename
data.to_csv(convertedFile,columns=vital_columns,header=vital_columns,index=False)