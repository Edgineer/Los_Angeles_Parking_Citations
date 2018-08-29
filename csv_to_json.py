import csv
import json
import argparse

#Add filename of CSV with data as command line argument
parser = argparse.ArgumentParser(description="Convert CSV file to JSON")
parser.add_argument('filename',type=str,help="filename of CSV file with LA Parking Citation Data to be converted")
arg = parser.parse_args()

#Read the CSV file and convert it into a list of JSON dictionaries
with open(arg.filename) as file:
	reader = csv.DictReader(file)
	rows = list(reader)

#Convert into JSON
convertedFile = "JSONtranslated_"+arg.filename
with open(convertedFile,'a+') as file1:
	json.dump(rows,file1,separators=(',',':'),indent=1)

#Remove the coma after each object and list braces and save to file
with open(convertedFile,'r+b') as file2:
	content = file2.read()
	content = content.replace('},', '}')
	content = content.replace('[', '')
	content = content.replace(']', '')
	file2.seek(0)
	file2.write(content)
	file2.truncate()