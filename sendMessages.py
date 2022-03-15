import csv
from tempfile import NamedTemporaryFile
import shutil
import secrets
import string

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

fileMailPassword = 'users.csv'
tempFile = NamedTemporaryFile('w+t', newline='', delete=False)

def sendEmail(email, passwd):
    server = 'smtp.mail.ru'
    user = "user@mail.ru"
    emailPassword = "password"

    recipients = email
    sender = user
    subject = "Enterprise password manager"
    text = 'Hello. <br>' \
           'The systems password manager is accessed at https://psono.test.com/. <br>' \
           'To be able to recover the password, it is recommended to generate a password recovery code in the account settings in the "Generate Password Recovery" tab and save it. <br>' \
           'Login: ' + email + '<br>' + 'Pass: ' + passwd + '<br>'
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, emailPassword)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()

if __name__ == '__main__':
    with open(fileMailPassword) as csvFile, tempFile:
        reader = csv.DictReader(csvFile, delimiter=';')
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(tempFile, fieldnames=fieldnames, delimiter=';', )
        writer.writeheader()

        for row in reader:
            if ((row['User created'] != 'Yes') and (row['Email'] != '') and (row['Pass'] != '')):
                sendEmail(row['Email'], row['Pass'])
                row['User created'] = 'Yes'
            print(row)
            writer.writerow(row)

    shutil.move(tempFile.name, fileMailPassword)


