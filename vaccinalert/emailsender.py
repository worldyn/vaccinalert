# Import smtplib for the actual sending function
import smtplib
import dbutils 
import json

message_notif = """\
Subject: 1177 vaccination page changed in your region

This mail was sent to you because you had signed up for the vaccine alert mail list. Please check the 
1177 vaccination page as it has been updated.\n Regards,\nvaccinalert"""

message_verify = """\
Subject: vaccinalert recieved your payment 

Hello!

This mail was sent to you because you have signed up for the vaccine alert mail list and paid with swish.

Please check your email on a daily basis to get the email notification when something has changed on the 1177 vaccination page.
\n\n Regards,\nvaccinalert"""


# tupformat input: (('mail@mail.com'), (), ...)
# not tupformat input: ['mail@mail.com', ...]
def send(receivers,message, tupformat=True):

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # open json file with mails 
    f = open('gmailaccountnames.json', 'r')
    data = json.load(f)
    sender_email = data["sender_email"]

    # Authentication
    s.login(data["sender_email"], data["sender_psw"])

    f.close()

    # sending the mail
    for email in receivers:
        if tupformat:
            s.sendmail(sender_email, email[0], message)
        else:
            s.sendmail(sender_email, email, message)
    
    # terminating the session
    s.quit()



def send_emails_notif(selected_region):
    db,cursor = dbutils.connect()
    res = dbutils.get_all_verified_emails(selected_region, db, cursor)

    send(res, message_notif)

# assumes list of emails exist in db
def send_emails_verified(email_list):
    #f = open('verifiedlist.json', 'r')
    #data = json.load(f)
    #email_list = data["emails"]
    #f.close()

    #db,cursor = dbutils.connect()
    #res = dbutils.get_all_verified_emails(selected_region, db, cursor)
    send(email_list, message_verify, tupformat=False)


# test
#send_emails("stockholm")
#send_emails_verified()
