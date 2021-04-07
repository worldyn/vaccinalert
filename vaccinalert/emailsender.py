# Import smtplib for the actual sending function
import smtplib
import dbutils 
import json

message = """\
Subject: 1177 vaccination page changed in your region

This mail was sent to you because you had signed up for the vaccine alert mail list. Please check the 
1177 vaccination page as it has been updated.\n Regards,\nwww.vaccinalert.se"""


def send(receivers):

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
        s.sendmail(sender_email, email[0], message)
    
    # terminating the session
    s.quit()



def send_emails(selected_region):

    db,cursor = dbutils.connect()
    res = dbutils.get_all_verified_emails(selected_region, db, cursor)

    send(res)


# test
#send_emails("stockholm")