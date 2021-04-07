# Import smtplib for the actual sending function
import smtplib

sender_email = "vaccinalert1@gmail.com"
receiver_email = "gustafholmeri@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""


# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
s.starttls()
  
# Authentication
s.login(sender_email, "weqnu5-myjmaf-jYsqom")
  

  
# sending the mail
s.sendmail(sender_email, receiver_email, message)
  
# terminating the session
s.quit()