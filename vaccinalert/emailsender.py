# Import smtplib for the actual sending function
import smtplib
import dbutils 
import json
import time

message_notif = """\
Subject: 1177 vaccination page changed in your region

This mail was sent to you because you had signed up for the vaccine alert email list.\nPlease check the 1177 vaccination page as it has been updated.\n\nRegards,\nvaccinalert"""

message_verify = """\
Subject: vaccinalert received your payment 

Hello!

This mail was sent to you because you have signed up for the vaccine alert email list and paid with swish or paypal.

Please check your email on a daily basis to get the email notification when something has changed on the 1177 vaccination page.
\n\nRegards,\nvaccinalert"""

# add a timestamp and error string with message_support.format()  
message_support = """\
Subject: vaccinalert  err

Check logs, at time {}, something went wrong in the scraping: {} """


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
    it = 0
    ratelimit = 15 # MIGHT HAVE TO BE TUNED
    ratelimit_sleep = 61
    for email in receivers:
        time.sleep(1)
        if tupformat:
            s.sendmail(sender_email, email[0], message)
        else:
            s.sendmail(sender_email, email, message)
        it += 1
        if it == ratelimit:
            print("rate limit hit, sleeping seconds: ", ratelimit_sleep)
            time.sleep(ratelimit_sleep)
            it = 0
    
    # terminating the session
    s.quit()

# send err notif to 
def send_support(timestamp, error_string):

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # open json file with mails 
    f = open('support_email_credential.json', 'r')
    data = json.load(f)
    sender_email = data["sender_email"]

    # Authentication
    s.login(data["sender_email"], data["sender_psw"])

    f.close()

    f = open('support_email.json', 'r')
    data = json.load(f)
    recv_email = data["support_email"]

    f.close()

    # sending the mail
    s.sendmail(sender_email, recv_email, message_support.format(timestamp, error_string))
        
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
