import requests
import csv
import json

#read in credential from file(for security) and store in variables
cred = open("credentials.txt","r")
credString = cred.readline()
credArray = credString.split(',',3)

username = credArray[0]
password = credArray[1]
url = credArray[2]

#use credentials to ask for token from API for authentication using credentials
r = requests.post(url + "/uapi/auth/tokens", auth=(username, password))
response = r.text

#parse/store token in variable
token = response.split('"',4)[3]

print(r.text)

#iterate through csv containing serials and new names
with open('Ipad inventory - Jack Scripts for LoL.csv', newline='') as csvfile:
  spamreader = csv.DictReader(csvfile)
  for row in spamreader:
    print(row['Serial'] + " " + row['Name'])
    serialNum = row['Serial']
    newName = row['Name']

    header = {'Authorization': 'Bearer ' + token}
    searchparam = {
      "pageNumber": 0,
      "pageSize": 100,
      "isLoadToEnd": False,
      "orderBy": [
        {
          "field": "Name",
          "direction": "DESC"
        }
      ],
      "serialNumber": serialNum
    }

    #search using API for device with serial number from csv
    h = requests.post(url + "/uapi/v1/search-mobile-devices",headers=header,json=searchparam)
    responseSearch = h.text
    SearchJson = json.loads(responseSearch)

    #parse ID from returned device
    currentID = str(SearchJson['results'][0]['id'])

    newNameParam = {
      "name": newName
    }

    #use device ID to rename device
    h = requests.post(url + "/JSSResource/mobiledevicecommands/command/DeviceName/" + newName + "/id/" + currentID,auth=(username, password))

    responseChange = h.text
    print(responseChange)