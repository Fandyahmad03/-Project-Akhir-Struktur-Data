import requests
import json


BASE_URL = "http://localhost:5000"

def test_register():
    data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    try:
        res_json = response.json()
    except Exception:
        print("Register Response Error:", response.text)
        return None
    print("Register Response:", res_json)
    return res_json.get("user_id")




def test_upload(user_id):
    metadata = {
        "camera": "Canon",
        "ai-engine": "FakeGAN",
        "resolution": "1920x1080",
        "x-fake-score": 0.85
    }
    data = {
        "user_id": user_id,
        "filename": "fake_video.mp4",
        "metadata": metadata
    }
    response = requests.post(f"{BASE_URL}/upload", json=data)
    try:
        print("Upload Response:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Upload Response Error:", response.text)

def test_high_risk():
    response = requests.get(f"{BASE_URL}/high-risk")
    try:
        print("High Risk Contents:", json.dumps(response.json(), indent=2))
    except Exception:
        print("High Risk Contents Error:", response.text)

def test_spread_map():
    response = requests.get(f"{BASE_URL}/spread-map")
    try:
        print("Spread Map:", json.dumps(response.json(), indent=2))
    except Exception:
        print("Spread Map Error:", response.text)

if __name__ == "__main__":
    user_id = test_register()
    if user_id:
        test_upload(user_id)
    test_high_risk()
    test_spread_map()