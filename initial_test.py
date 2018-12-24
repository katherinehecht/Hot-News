#! /usr/bin/env python3
import requests
import json
# Init
api_key = 'dc144ea3dc104ccf987920e4f4475c27'

stateNames = []
stateAbbreviations = []
with open("states.csv") as f:
    for line in f:
        print(line)
        line = line.split(",")
        stateNames.append(line[0])
        stateAbbreviations.append(line[1].strip())
       # stateAbbreviations = [i[1] for i.split(",") in line]

print(str(stateNames))
print(str(stateAbbreviations))
# print(str(stateAbbreviations))

r = requests.get("".join(["https://newsapi.org/v2/top-headlines?country=us&apiKey=", api_key]))
resp = json.loads(r.content.decode())
print(resp['totalResults'])
