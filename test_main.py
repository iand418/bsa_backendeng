from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'Welcome': 'Hotel Industry'}
    
def test_read_events():
    response = client.get("/events/2607?room_reservation_id=0024cd80-6d7d-46b5-9e8e-ae51012d0daf")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 19182231,
        "hotel_id": 2607,
        "room_reservation_id": "0024cd80-6d7d-46b5-9e8e-ae51012d0daf",
        "night_of_stay": "2022-03-12",
        "event_timestamp": "2022-03-07T19:01:03",
        "status": 1
    }]

def test_create_event():
    response = client.post(
        "/events/",
        json={"id": 32168693,
            "hotel_id": 2601,
            "room_reservation_id": "0024cd80-6d7d-46b5-9e8e-ae51012d0dad",
            "night_of_stay": "2024-09-20",
            "event_timestamp": "2024-09-20T18:45:03",
            "status": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 32168693,
        "hotel_id": 2601,
        "room_reservation_id": "0024cd80-6d7d-46b5-9e8e-ae51012d0dad",
        "night_of_stay": "2024-09-20",
        "event_timestamp": "2024-09-20T18:45:03",
        "status": 1,
    }

def test_dashboard():
    response = client.get("/dashboard/2607?year=2022&monthly=true")
    assert response.status_code == 200
    assert response.json() =={
                    "1": 21847,
                    "2": 5145,
                    "3": 13905,
                    "4": 5841,
                    "5": 7852,
                    "6": 5318,
                    "7": 3611,
                    "8": 22,
                    "10": 2,
                    "11": 1,
                    "12": 2
    }