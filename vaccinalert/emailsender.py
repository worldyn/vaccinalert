# Import smtplib for the actual sending function
import smtplib
import dbutils 


message = """\
Subject: Hi there

This message is sent from Python."""


def send(receivers):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    

    f = open('gmailaccountnames.json', 'r')
    data = json.load(f)

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
send_emails("stockholm")