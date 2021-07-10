import requests
import smtplib
from  edugame.settings import MAILGUN_ENDPOINT, MAILGUN_API


def send_mail(mail_id,message):
    
    res = requests.post(
    MAILGUN_ENDPOINT,
    auth=("api", MAILGUN_API),
    data={"from": "No-Reply <no-reply@covidsupport.live>",
            "to": [mail_id],
            "subject": "Don't Reply",
            "text": message})

    print(res.text)

