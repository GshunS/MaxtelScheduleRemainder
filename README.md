# MaxtelScheduleRemainder

**MaxtelScheduleRemainder** is a Python script that automates the process of retrieving the newest Maxtel shifts, calculating total work hours, estimating pay, and sending email notifications. It's designed to save you time and effort by eliminating manual calculations.

## Features

1. **Shift Data Retrieval**:
   - The script uses the `requests` package to fetch shift data from the Maxtel API.
   - You'll need to provide your Maxtel API endpoint or URL in the script.

2. **Work Hours Calculation**:
   - After retrieving the shift data, **MaxtelScheduleRemainder** calculates the total work hours.
   - It considers start and end times for each shift.

3. **Estimated Pay**:
   - Based on the total work hours and any relevant pay rates, the script estimates your earnings.
   - You can customize pay rates or use predefined values.

4. **Email Notifications**:
   - Once the calculations are complete, the script sends an email to your specified address.
   - Make sure to configure your email settings (SMTP server, credentials, etc.) within the script.
   
## Automating with Windows Task Scheduler

To automate the execution of your **MaxtelScheduleRemainder** script on a Windows machine, follow these steps:

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and hit Enter.
   - Alternatively, search for "Task Scheduler" in the Start menu.

2. **Create a New Task**:
   - In the right-hand pane, click on "Create Basic Task..." or "Create Task..." (depending on your Windows version).
   - Follow the wizard to set a name and description for your task.

3. **Trigger Settings**:
   - Choose how often you want the script to run (e.g., daily, weekly, etc.).
   - Set the start time and any other relevant options.

4. **Action Settings**:
   - Select "Start a Program" as the action.
   - Browse to the location of your Python executable (usually `python.exe`).
   - In the "Add arguments" field, specify the path to the `RetrieveSchedule.py` script

5. **Conditions and Settings**:
   - Configure any additional conditions or settings (e.g., only run when the computer is idle).

6. **Test the Task**:
   - Right-click on your newly created task and choose "Run" to verify that it works as expected.

Remember to adjust the paths and settings according to your specific setup. Once configured, the Task Scheduler will automatically run your script at the specified intervals.


## Dependencies

- Python 3.x
- `requests` package (for API requests)
- SMTP server (for email notifications)

## Disclaimer

Remember to handle sensitive information (such as API keys and email credentials) securely.

