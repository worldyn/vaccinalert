import json
import time
from dbutils import *
from emailsender import *

def main():
    # load emails
    print("Loading emails...")
    f = open('verifiedlist.json', 'r')
    data = json.load(f)
    email_list = data['emails']
    f.close()
    print("emails loaded...")

    print("checking emails...")
    db, cursor = connect()
    emails_valid, emails_invalid = check_emails(email_list, db, cursor)

    print("Valid emails: ", emails_valid)
    if len(emails_invalid) > 0:
        print("Emails does not exist: ", emails_invalid)
    else:
        print("All emails valid...")

    print("updating verified status...")
    ok = verify_emails(emails_valid, db, cursor)
    if not ok:
        print("error verifying emails in db, exiting...")
        db.close()
        return

    print("sending verification emails...")
    send_emails_verified(emails_valid) 

    db.close()
    
if __name__ == "__main__":
    main()
