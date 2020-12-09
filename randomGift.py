import os
import smtplib
import imaplib
import email
import random
from email.message import EmailMessage

# gmail login information
EMAIL_ADDRESS = os.environ.get('GM_USER')
EMAIL_PASSWORD = os.environ.get('GM_PASSWORD')

# read text file for name and emails
people = []
emails = []
file = open('participants.txt', 'r')
while True:
    holder = file.readline().rstrip('\n')
    if (holder == ""):
        file.close()
        break
    else:
        emails.append(holder)
        people.append(file.readline().rstrip('\n'))

# shuffle people's list
# using Fisher–Yates shuffle Algorithm 
# to shuffle a list 
for i in range(len(people)-1, 0, -1):
    j = 0
    while (i == j):
        # Pick a random index from 0 to i  
        j = random.randrange(i + 1)
    
    # Swap arr[i] with the element at random index  
    people[i], people[j] = people[j], people[i]

# send random name to each email
for e in emails:
    # form email
    email = EmailMessage()
    email['Subject'] = 'The Person You Will Gift To Is.......'
    email['From'] = EMAIL_ADDRESS
    email['To'] = e
    email.set_content(people[emails.index(e)])

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # log in to gmail account
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # send the email
        smtp.send_message(email)
        # report
        print("Mail sent to: " + people[emails.index(e)])

        smtp.quit()

# delete sent emails to maintain full autonomous
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
imap.select('"[Gmail]/Sent Mail"')
status, mails = imap.search(None, 'SUBJECT "The Person You Will Gift To Is......."')
mails = mails[0].split(b' ')
for mail in mails:
    print("Deleting: " + mail.decode())
    imap.store(mail, "+FLAGS", "\\Deleted")
# permanantly delete all flagged deleted
imap.expunge()
imap.close()
imap.logout()



""" TO CHECK DIFFERENT MAILBOX 
for i in mail.list()[1]:
    print(i)
"""

""" TEMPLATE 
# form email information
email = EmailMessage()
email['Subject'] = 'The Person You Will Gift To Is.......'
email['From'] = EMAIL_ADDRESS
email['To'] = EMAIL_ADDRESS
email.set_content('<PERSON NAME>')

# establish connection with gmail and send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    # log in to gmail account
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # send the email
    smtp.send_message(email)
"""