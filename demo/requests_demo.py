# uv add requests
import requests

url = 'http://127.0.0.1:8000/dar/user/login'

data = {
    'user_name': 'test01',
    'passwd': 'admin123'
}

response = requests.post(url, data=data)

print(response.text)
