import smtplib

class EmailSender(object):
    def __init__(self, sender_id, sender_pass):
        self.sender_id = sender_id
        self.sender_pass = sender_pass

    def send(self, message):
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(self.sender_id, self.sender_pass)
        # message to be sent
        msg = f"Subject: New Maxtel Shifts\n\n{message}"
        # sending the mail
        s.sendmail(self.sender_id, self.sender_id, msg)
        # terminating the session
        s.quit()

