import os
import smtplib
from dotenv import load_dotenv

def send_email(alert_message: str, subject:str='Sent from python') -> None:
    load_dotenv()

    email_address = os.getenv('EMAIL_ADDRESS')
    email_pwd = os.getenv('EMAIL_PASSWORD')

    print(email_address)
    

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_address, email_pwd)

        body = 'This email was sent from python'

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(email_address, email_address, msg)


if __name__ == '__main__':
    send_email('')