import smtplib
import ssl
import os


class Email:
    def send_email(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "cabrerajaime877@gmail.com"
        password = "leuayokgevolnkdn"

        receiver = "cabrerajaime877@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)
        print("Email was sent!")
