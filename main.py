import requests
from time import sleep

api_url = "http://example.com"
vehicles_api_url = api_url + "/vehicles"

def create_vehicle(sleepiness: int, latitude: float, longitude: float):
    body = {
        "heading": 0,
        "sleepiness": sleepiness,
        "vehicle_type": {
            "type": "SUV",
            "color": "white"
        },
        "coordinate": {
            "latitude": latitude,
            "longitude": longitude
        }
    }
    requests.post(vehicles_api_url, json=body)


# main

# load json
sleepiness = 4
speed = 1
root = [
    {"latitude": 0, "longitude": 0},
    {"latitude": 10, "longitude": 10},
]

# 5秒で進む距離
distance_in_5sec = speed * 5

# init
create_vehicle(sleepiness, root[0]["latitude"], root[0]["longitude"])
current_lat = root[0]["latitude"]
current_long = root[0]["longitude"]

# run
running_road = 0
while True:
    try:
        print(f"Running from point {running_road} to point {running_road + 1}")
    except KeyboardInterrupt:
        # stop
        print("Stopped")
    
