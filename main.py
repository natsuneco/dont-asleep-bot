import sys
import requests
import json
import time
import math

# API のベース URL
API_BASE_URL = "http://160.16.135.208"

# 車両の作成
def create_vehicle(sleepiness=4, type="sedan", color="red"):
    url = f"{API_BASE_URL}/vehicles"
    payload = {
        "heading": 0,
        "sleepiness": sleepiness,
        "latitude": 0,
        "longitude": 0,
        "vehicle_type": {
            "type": type,
            "color": color
        }
    }
    response = requests.post(url, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()["id"]  # 作成された車両のIDを返す

# 車両の更新
def update_vehicle(vehicle_id, latitude, longitude, heading):
    url = f"{API_BASE_URL}/vehicles/{vehicle_id}"
    payload = {
        "heading": heading,
        "latitude": latitude,
        "longitude": longitude
    }
    response = requests.patch(url, data=json.dumps(payload))
    response.raise_for_status()

# 車両の削除
def delete_vehicle(vehicle_id):
    url = f"{API_BASE_URL}/vehicles/{vehicle_id}"
    response = requests.delete(url)
    response.raise_for_status()

# 座標間の距離を計算
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球の半径 (メートル)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # メートル単位の距離
    return distance

# 2つの座標間の方角を計算
def calculate_heading(lat1, lon1, lat2, lon2):
    delta_lon = lon2 - lon1
    y = math.sin(math.radians(delta_lon)) * math.cos(math.radians(lat2))
    x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon))
    heading = math.atan2(y, x)
    return math.degrees(heading)

# 車両を等速で移動させる
def move_vehicle(vehicle_id, route, speed=10, interval=1):
    while True:
        try:
            for i in range(len(route)):
                start_lat, start_lon = route[i]["latitude"], route[i]["longitude"]
                end_lat, end_lon = route[(i + 1) % len(route)]["latitude"], route[(i + 1) % len(route)]["longitude"]
                distance = calculate_distance(start_lat, start_lon, end_lat, end_lon)
                steps = max(1, distance / (speed * interval))  # 更新回数
                lat_step = (end_lat - start_lat) / steps
                lon_step = (end_lon - start_lon) / steps

                current_lat = start_lat
                current_lon = start_lon

                for _ in range(int(steps)):
                    heading = calculate_heading(current_lat, current_lon, end_lat, end_lon)
                    update_vehicle(vehicle_id, current_lat, current_lon, heading)
                    # print(current_lat, current_lon)
                    current_lat += lat_step
                    current_lon += lon_step
                    time.sleep(interval)
        except KeyboardInterrupt:
            delete_vehicle(vehicle_id)
            print(f"Vehicle {vehicle_id} was deleted")
            break

# メイン処理
if __name__ == "__main__":
    # JSON ファイルの読み込み
    json_data = None
    try:
        json_path = sys.argv[1]
        with open(json_path) as f:
            json_data = json.load(f)
    except IndexError:
        print("Please specify JSON file")
    
    vehicle_id = create_vehicle(json_data["sleepiness"], json_data["vehicle_type"]["type"], json_data["vehicle_type"]["color"])
    print(f"Vehicle created with ID: {vehicle_id}")
    
    # 経路の指定
    route = json_data["route"]

    # 車両を巡回させる
    move_vehicle(vehicle_id, route, speed=10, interval=1)
