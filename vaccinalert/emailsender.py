# Import smtplib for the actual sending function
import smtplib

sender_email = "vaccinalert1@gmail.com"

# take from database
receiver_emails = ["gustafholmeri@gmail.com", "gustaf.holmer@outlook.com"] 

message = """\
Subject: Hi there

This message is sent from Python."""


def send_emails():
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(sender_email, "weqnu5-myjmaf-jYsqom")
    

    
    # sending the mail
    for email in receiver_emails:
        s.sendmail(sender_email, email, message)
    
    # terminating the session
    s.quit()


send_emails()