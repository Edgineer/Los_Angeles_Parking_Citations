import pandas as pd
import requests
import json

#Read CSV file containing US Feet Coordinates
data = pd.read_csv('Parking_Citations_sample.csv')
data.head()
lat = data['Latitude'].values
lon = data['Longitude'].values

#File to extract cordinates and format for API request
filo = open('formattedCoords.txt', 'a+')
for la,lo in zip(lat,lon):
	filo.write(str(la)+','+str(lo)+';')
filo.close()

#API URL
http = str('http://epsg.io/trans?data=')
#Codes for conversion from US Feet Coordinates to World Geodetic System 1984
attr = str('&s_srs=102645&t_srs=4326')
with open("formattedCoords.txt", "r") as file:
	coords = file.read()
file.close()

#Making HTTP Request to the API
url = http + coords + attr
url = url.replace(';&s_srs', '&s_srs')
page = requests.get(url)
content = page.content

print "Response Code:"
print page.status_code

print "=================================================Response Body==========================================="
resData = json.loads(content)
lats = []
lons = []
for d in resData:
	lats.append(d.get("y"))
	lons.append(d.get("x"))
print lats
print lons


dic = {'lat':lats,'lon':lons}
df = pd.DataFrame(dic)

data['Latitude'] = df['lat']
data['Longitude'] = df['lon']
print data.head(5)
vital_columns = ["Ticket number","Issue Date","Issue time","Make","Body Style","Color","Location","Violation code","Violation Description","Fine amount","Latitude","Longitude"]
data.to_csv("Parking_Citations_sample_trans.csv",columns=vital_columns,header=vital_columns,index=False)