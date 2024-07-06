import smtplib

class EmailSender(object):
    def __init__(self):
        pass

    def testEmail(self):
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("guoshun.su@gmail.com", "sqpu kmge bacz wqlx")
        # message to be sent
        message = "Hi, email"
        # sending the mail
        s.sendmail("guoshun.su@gmail.com", "guoshun.su@gmail.com", message)
        # terminating the session
        s.quit()