import requests
import unittest



class SendRequests:
    def __init__(self):
        pass

    def _make_request(self, method, url, data, headers):
        if not isinstance(method, str) or method.upper() not in ['GET', 'POST']:
            raise ValueError("Invalid method")

        if not isinstance(url, str) or not url.strip():
            raise ValueError("Invalid URL")

        try:
            if headers is None:
                res = requests.request(method=method, url=url, params=data if method.upper() == 'GET' else None, data=data if method.upper() == 'POST' else None)
            else:
                res = requests.request(method=method, url=url, params=data if method.upper() == 'GET' else None, data=data if method.upper() == 'POST' else None, headers=headers)
            return res.json()
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def run_main(self, method, url, data, headers):
        return self._make_request(method, url, data, headers)

class TestSendRequests(unittest.TestCase):
    def test_login(self):
        url = 'http://127.0.0.1:8000/dar/user/login'
        data = {
            'user_name': 'test01',
            'passwd': 'admin123'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # 使用 SendRequests 类来发送请求
        request_sender = SendRequests()
        response = request_sender.run_main('POST', url, data, headers)
        
        # 断言状态码
        self.assertEqual(response['msg_code'], 200, "Login failed")
        
if __name__ == '__main__':
    unittest.main()