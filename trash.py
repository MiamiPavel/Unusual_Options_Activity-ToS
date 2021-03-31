import yagmail
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
subject_wip = str(today) + " Unusual Stock Options Activity for Today - By Ticker"

#print(subject_wip)


# Send email functionality
receiver = "plitv001+stock@gmail.com"
subject = subject_wip
body = "test"

yag = yagmail.SMTP("plitv001@gmail.com","origivxvqatmkkzc")
yag.send(
    to=receiver,
    subject= subject,
    contents=body)
print("Email Sent")