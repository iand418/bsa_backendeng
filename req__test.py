import requests, json
url = 'http://localhost:8000/events/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {
    "id": 32168694,
    "hotel_id": 2601,
    "room_reservation_id": "0024cd80-6d7d-46b5-9e8e-ae51012d0ddd",
    "night_of_stay": "2024-09-21",
    "event_timestamp": "2024-09-20T18:45:03",
    "status": 1,
}
response = requests.post(url, data=json.dumps(data),headers=headers)
print(response)