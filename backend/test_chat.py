import os
import requests

PORT = os.getenv("PORT", "8000")
URL = f"http://127.0.0.1:{PORT}/chat"

try:
    r = requests.post(URL, data={'user_id': 'test', 'thread_id': 'thread_test', 'message': 'hello'})
    print('STATUS:', r.status_code)
    print('BODY:', r.text)
except requests.exceptions.ConnectionError:
    print(f"Connection failed: Ensure FastAPI server is running on port {PORT}")

