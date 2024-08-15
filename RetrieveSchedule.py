import datetime
import os

import requests
# from Login import Login
from dotenv import load_dotenv

from CalculateTax import calculateTax
from SendEmail import EmailSender


class schedule(object):
    def __init__(self, username, password, start_date, selected_date):
        self.es = EmailSender(os.getenv('MY_USERNAME'), os.getenv('MY_maxtelGmailPassword'))
        self.username = username
        self.password = password
        self.WeekStartDate = start_date
        self.SelectedDate = selected_date
        self.hourly_rate = 23.25
        self.weekday_dict = {
            0: 'Mon',
            1: 'Tue',
            2: 'Wed',
            3: 'Thu',
            4: 'Fri',
            5: 'Sat',
            6: 'Sun'
        }
        self.headers = {
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json',
            'Referer': 'https://mcd.maxtel.com/EmployeeMobile/Home',
            'X-CSRFToken': os.getenv('MY_X-CSRFToken'),
            'sec-ch-ua-platform': '"Windows"',
        }

        self.json_data = {
            'versionInfo': {
                'moduleVersion': os.getenv('MY_moduleVersion'),
                'apiVersion': os.getenv('MY_apiVersion'),
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
        start_date = datetime.datetime.strptime(self.WeekStartDate, "%Y-%m-%d")
        end_date = start_date + datetime.timedelta(days=6)
        if len(schedules) == 0:
            message = f'No Shifts ' \
                      f'from ({self.weekday_dict[start_date.weekday()]}) {start_date} ' \
                      f'to ({self.weekday_dict[end_date.weekday()]}) {end_date}'
            return message, False
        else:
            message = f'Your Shifts ' \
                      f'from ({self.weekday_dict[start_date.weekday()]}) {start_date} ' \
                      f'to ({self.weekday_dict[end_date.weekday()]}) {end_date} are \n'
            total_hours = 0
            for shift in schedules:
                start_time = datetime.datetime.strptime(
                    shift['LightShift']['StartDateTime'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=12)
                end_time = datetime.datetime.strptime(
                    shift['LightShift']['EndDateTime'], '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=12)
                duration = (end_time - start_time).total_seconds() / 60 / 60
                message += f'({self.weekday_dict[start_time.weekday()]}) {start_time} - ' \
                           f'({self.weekday_dict[end_time.weekday()]}) {end_time} - ' \
                           f'{round(duration, 2)} hours\n'
                total_hours += duration
            total_paid_hours = total_hours - len(schedules) * 0.5
            message += f'\nTotal Working Hours is {round(total_hours, 2)}\n'
            message += f'\nTotal Paid Hours is {round(total_paid_hours, 2)}\n'
        total_paid = total_paid_hours * self.hourly_rate
        calTax = calculateTax(total_paid)
        total_paid = calTax.calculate()

        message += f'\nEstimated Total Paid is {round(total_paid, 2)}\n'
        return message, True

    def start(self):
        # login_session = self.getSession()
        data = self.getSchedule()
        result = self.dataProcessing(data)
        if result[1]:
            write_f = open('shifts.txt', 'a')
            write_f.writelines('\n' + self.WeekStartDate)
            write_f.close()
            self.es.send(result[0])

if __name__ == '__main__':
    load_dotenv()

    f = open('./shifts.txt', 'r')
    WeekStartDate = [line.strip() for line in f.readlines()][-1]
    f.close()

    WeekStartDate = datetime.datetime.strptime(WeekStartDate, "%Y-%m-%d") + datetime.timedelta(days=7)
    WeekStartDate = datetime.datetime.strftime(WeekStartDate, "%Y-%m-%d")
    SelectedDate = WeekStartDate
    rs = schedule('', '', WeekStartDate, SelectedDate)
    rs.start()
