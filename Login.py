import os

import requests
from dotenv import load_dotenv


class Login(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

        self.headers = {
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'Referer': 'https://mcd.maxtel.com/EmployeeMobile/',
            'X-CSRFToken': os.getenv('MY_X-CSRFToken'),
            'sec-ch-ua-platform': '"Windows"',
        }
        self.json_data = {
            'versionInfo': {
                'moduleVersion': os.getenv('MY_moduleVersion'),
                'apiVersion': os.getenv('MY_apiVersion'),
            },
            'viewName': 'Common.Login',
            'inputParameters': {
                'Username': f'{self.username}',
                'Password': f'{self.password}',
                'IsPWA': False,
            },
        }

    def run(self):
        response = self.session.post(
            'https://mcd.maxtel.com/EmployeeMobile/screenservices/Access_MCW_v2/Blocks/LoginFeature/ActionDoLogin',
            headers=self.headers,
            json=self.json_data,
        )
        # print(response.json()['exception']['message'])
        print(response.json())
        return self.session


def test_run():
    load_dotenv()
    user_name = os.getenv('MY_USERNAME')
    pwd = os.getenv('MY_PASSWORD')

    log = Login(user_name, pwd)
    log.run()


if __name__ == '__main__':
    test_run()
