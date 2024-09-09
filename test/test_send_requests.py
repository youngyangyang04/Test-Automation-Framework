import pytest
from unittest.mock import patch
from common.send_requests import SendRequests

class TestSendRequests:

    def setup_method(self):
        self.send_requests = SendRequests()
        self.url = "http://example.com"
        self.data = {"key": "value"}
        self.headers = {"Content-Type": "application/json"}

    def test_run_main_get(self):
        # Mock the get method
        with patch('send_requests.SendRequests.get') as mock_get:
            mock_get.return_value = 'mocked response'
            res = self.send_requests.run_main('GET', self.url, self.data, self.headers)
            mock_get.assert_called_once_with(self.url, self.data, self.headers)
            assert res == 'mocked response'

    def test_run_main_post(self):
        # Mock the post method
        with patch('send_requests.SendRequests.post') as mock_post:
            mock_post.return_value = 'mocked response'
            res = self.send_requests.run_main('POST', self.url, self.data, self.headers)
            mock_post.assert_called_once_with(self.url, self.data, self.headers)
            assert res == 'mocked response'

    def test_run_main_unsupported_method(self):
        res = self.send_requests.run_main('PUT', self.url, self.data, self.headers)
        assert res is None  # Assuming the method returns None when unsupported

    def teardown_method(self):
        self.send_requests = None

if __name__ == '__main__':
    pytest.main()