import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

dt=datetime.today()
day=dt.day
month=dt.month
year=dt.year
sender_email = "attendance.srmitktr@gmail.com"
receiver_email = "sm7283@srmist.edu.in"
password = "srmitktr"

message = MIMEMultipart("alternative")
message["Subject"] = "Faculty Attendance on "+str(day)+' - ' +str(month)+' - '+str(year)
message["From"] = sender_email
message["To"] = receiver_email


text='The following Attachment is the list of Faculties who were present on ' +str(day)+' - ' +str(month)+' - '+str(year) +'\n\n\n\n Regards \n Smart Attendance System. '
body_part = MIMEText(text, 'plain')

message.attach(body_part)
with open('Attendance.csv','rb') as file:
    message.attach(MIMEApplication(file.read(), Name="Attendance.csv"))
print('Email Sent')
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

    #"meenaksk@srmist.edu.in"