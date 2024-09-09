import pytest
from common.send_requests import SendRequests
def test_login():
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
    assert response['msg_code'] == 200, "Login failed"