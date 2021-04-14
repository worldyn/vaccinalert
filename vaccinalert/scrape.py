import requests 
#from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
from dbutils import *
from emailsender import *
import random
import warnings

def main():
    sleep_time = 100 # seconds
    print("=> script.py started ...")

    while True:
        #print("\n\n")
        #print("=> Scraping 1177.se")

        # setup web browser
        #warnings.simplefilter("ignore")
        browser = webdriver.PhantomJS()
        # sthlm hardcoded
        #url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
        url = 'https://www.1177.se/'
        browser.get(url)

        boxes = browser.find_elements_by_css_selector(".c-teaser-outer .c-image img")
        num_boxes = len(boxes)
        #print("=> Number of boxes: ", num_boxes)

        not_open = "annu-inte-oppen" # hardcoded stuff sthlm
        num_notopen = 0
        for i,box in enumerate(boxes):
            imgsrc = box.get_attribute("src")
            if not_open in imgsrc:
                num_notopen += 1

        print("=> scraped box {}, scrape closed".format(num_boxes, num_notopen))

        if num_boxes >= num_notopen and num_notopen != 0 and num_boxes != 0:
            #print("=> Checking db status...")
            try:
                db, cursor = connect()
                curr_num_groups, curr_num_closed_groups = get_status("stockholm", db,cursor)
                print("=>scraped box {}, scrape closed {}, curr #groups {}, curr # closed groups {}".format(num_boxes, num_notopen,curr_num_groups, curr_num_closed_groups))

                # if mismatch send out emails and update db
                if curr_num_groups >= curr_num_closed_groups and type(curr_num_groups) == int and type(curr_num_closed_groups) == int and curr_num_closed_groups > num_notopen:
                    print("=> ALERT MISMATCH!!! Sending out alerts ...")
                    send_emails_notif("stockholm")
                    update_status("stockholm", num_boxes, num_notopen, db, cursor)
            except:
                print("Database error / could not reach...")
                # send mail to support! 
                f = open('support_email.json', 'r')
                data = json.load(f)
                support_email = data["support_email"]
                send(
                    [support_email], 
                    """\
Subject: vaccinalert db err

                    Database error vaccinalert.se, check log""",
                    tupformat=False
                )
        else:
            print("ERROR in scraping, num boxes {}, num closed {}".format(num_boxes, num_notopen))
                
        browser.quit()
        # sleepy time
        #print("=> Sleepy time for {} seconds... zzzzz".format(sleep_time))
        sleep = sleep_time + random.randrange(15) 
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
