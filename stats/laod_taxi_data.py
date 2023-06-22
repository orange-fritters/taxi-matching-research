import json
import urllib
import requests
import pandas as pd

data = pd.read_csv("data/20230227.csv")

with open('stats/config.json') as f:
    data = json.load(f)
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')

def get_coordinates(location, client_id, client_secret):
    url_location = str(urllib.parse.quote(location))
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={url_location}"
    
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urllib.request.urlopen(request)
    
    response_body = response.read().decode('utf-8')
    data = json.loads(response_body)        

    x = data["addresses"][0]['x']
    y = data["addresses"][0]['y']

    return x, y

def get_direction(start, goal, client_id, client_secret):
    start_x, start_y = get_coordinates(start, client_id, client_secret)
    goal_x, goal_y = get_coordinates(goal, client_id, client_secret)
    print(start_x)
    print(start_y)
    print(goal_x)
    print(goal_x)
    url = f"https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={start_x},{start_y}&goal={goal_x},{goal_y}&option=trafast"

    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)

    response = urllib.request.urlopen(request)
    response_body = response.read().decode('utf-8')
    data = json.loads(response_body)
    the_time = direction["route"]["trafast"][0]["summary"]["duration"]
    return the_time

# Sample usage

start = "상계1동"
goal = "하계1동"

the_time = get_direction(start, goal, client_id, client_secret)


