# MaxtelScheduleRemainder

**MaxtelScheduleRemainder** is a Python script that automates the process of retrieving Maxtel shifts, calculating total work hours, estimating pay, and sending email notifications. It's designed to save you time and effort by eliminating manual calculations.

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


## Dependencies

- Python 3.x
- `requests` package (for API requests)
- SMTP server (for email notifications)

## Disclaimer

Remember to handle sensitive information (such as API keys and email credentials) securely.

