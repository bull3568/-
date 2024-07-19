import requests

def get_coordinates(client_id, client_secret, address):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {
        'query': address
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['addresses']:
            x = data['addresses'][0]['x']  # 경도
            y = data['addresses'][0]['y']  # 위도
            return x, y
        else:
            print(f"주소를 찾을 수 없습니다: {address}")
            return None, None
    else:
        print("Failed to retrieve data:", response.status_code, response.text)
        return None, None

def get_driving_route(client_id, client_secret, start, goal):
    url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {
        'start': f"{start[0]},{start[1]}",
        'goal': f"{goal[0]},{goal[1]}",
        'option': 'trafast'  # 최적 경로 옵션
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code, response.text)
        return None

def print_route_duration(route_info, direction):
    if route_info and 'route' in route_info and 'trafast' in route_info['route']:
        duration_ms = route_info['route']['trafast'][0]['summary']['duration']
        duration_seconds = duration_ms // 1000  # 밀리초를 초로 변환
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"{direction} 이동 시간: {hours}시간 {minutes}분")
    else:
        print(f"{direction} 경로 정보를 가져올 수 없습니다.")

# 클라이언트 ID와 비밀번호
client_id = 
client_secret = 

# 주소를 입력하세요
start_address = '서울시 서초구 효령로 46길 21'
goal_address = '서울 구로구 디지털로32나길 22'

# 주소를 경도와 위도로 변환
start_coordinates = get_coordinates(client_id, client_secret, start_address)
goal_coordinates = get_coordinates(client_id, client_secret, goal_address)

if start_coordinates and goal_coordinates:
    # 출발지에서 도착지까지의 경로
    route_info_to = get_driving_route(client_id, client_secret, start_coordinates, goal_coordinates)
    print_route_duration(route_info_to, "출발지에서 도착지까지")

    # 도착지에서 출발지까지의 경로
    route_info_from = get_driving_route(client_id, client_secret, goal_coordinates, start_coordinates)
    print_route_duration(route_info_from, "도착지에서 출발지까지")
