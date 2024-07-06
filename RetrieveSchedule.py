import datetime
import os

import requests
# from Login import Login
from dotenv import load_dotenv

from CalculateTax import calculateTax


class schedule(object):
    def __init__(self, username, password, start_date, selected_date):
        self.username = username
        self.password = password
        self.WeekStartDate = start_date
        self.SelectedDate = selected_date
        self.hourly_rate = 23.25
        self.headers = {
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'Referer': 'https://mcd.maxtel.com/EmployeeMobile/Home',
            'X-CSRFToken': '2LnCJlyRNdvWB8amr3PA3QGk3I4=',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.json_data = {
            'versionInfo': {
                'moduleVersion': 'n+TH6jhnfk3ySmRPpNZpkA',
                'apiVersion': 'K2dH5PywXIDQ3mbXe1Jl_g',
            },
            'viewName': 'MainFlow.Home',
            'screenData': {
                'variables': {
                    'WeekStartDate': f'{self.WeekStartDate}',
                    'SelectedDate': f'{self.SelectedDate}',
                    '_selectedDateInDataFetchStatus': 1,
                },
            },
        }

    # def getSession(self):
    #     log = Login(self.username, self.password)
    #     login_session = log.run()
    #     return login_session

    def getSchedule(self):
        cookies = {
            'nr2Users': os.getenv('MY_nr2Users'),
            'nr1Users': os.getenv('MY_nr1Users')
        }
        response = requests.post(
            'https://mcd.maxtel.com/EmployeeMobile/screenservices/EmployeeMobile/ReusableWebBlocks/Schedule_Small/DataActionFetchShiftsForWeek',
            cookies=cookies,
            headers=self.headers,
            json=self.json_data
        )
        return response.json()

    def dataProcessing(self, data):
        schedules = data['data']['Out_LightShifts']['List']
        end_date = datetime.datetime.strptime(self.WeekStartDate, "%Y-%m-%d") + datetime.timedelta(days=7)
        if len(schedules) == 0:
            return f'No Shifts from {self.WeekStartDate} to {end_date}'
        else:
            message = f'Your Shifts from {self.WeekStartDate} to {end_date} are \n'
            total_hours = 0
            for shift in schedules:
                start_time = datetime.datetime.strptime(
                    shift['LightShift']['StartDateTime'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=12)
                end_time = datetime.datetime.strptime(
                    shift['LightShift']['EndDateTime'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=12)
                duration = (end_time - start_time).total_seconds() / 60 / 60
                message += f'{start_time} - {end_time} - {round(duration, 2)} hours\n'
                total_hours += duration
            total_paid_hours = total_hours - len(schedules) * 0.5
            message += f'\nTotal Working Hours is {round(total_hours, 2)}\n'
            message += f'\nTotal Paid Hours is {round(total_paid_hours, 2)}\n'
        total_paid = total_paid_hours * self.hourly_rate
        calTax = calculateTax(total_paid)
        total_paid = calTax.calculate()

        message += f'\nEstimated Total Paid is {round(total_paid, 2)}\n'
        return message

    def start(self):
        # login_session = self.getSession()
        data = self.getSchedule()
        return self.dataProcessing(data)


if __name__ == '__main__':
    load_dotenv()
    # user_name = os.getenv('MY_USERNAME')
    # pwd = os.getenv('MY_PASSWORD')

    today = datetime.datetime.today()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    next_monday = today + datetime.timedelta(days=days_until_monday + (-7))

    WeekStartDate = next_monday.strftime('%Y-%m-%d')
    SelectedDate = '2024-07-15'
    rs = schedule('', '', WeekStartDate, SelectedDate)
    print(rs.start())
