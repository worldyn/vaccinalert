import requests 
#from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
from dbutils import *
from emailsender import *

def main():
    sleep_time = 60 # seconds

    while True:
        print("\n\n")
        print("=> Scraping 1177.se")

        # setup web browser
        browser = webdriver.PhantomJS()
        # sthlm hardcoded
        url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
        browser.get(url)

        boxes = browser.find_elements_by_css_selector(".c-teaser-outer .c-image img")
        num_boxes = len(boxes)
        print("=> Number of boxes: ", num_boxes)

        not_open = "annu-inte-oppen" # hardcoded stuff sthlm
        num_notopen = 0
        for i,box in enumerate(boxes):
            imgsrc = box.get_attribute("src")
            if not_open in imgsrc:
                num_notopen += 1

        print("=> Number of closed boxes: ", num_notopen)
        
        print("=> Checking db status...")
        db, cursor = connect()
        curr_num_groups, curr_num_closed_groups = get_status("stockholm", db,cursor)
        print("=> Current number of groups {}, number of closed groups {}"\
                .format(curr_num_groups, curr_num_closed_groups))

        # if mismatch send out emails and update db
        if curr_num_groups != num_boxes or curr_num_closed_groups != num_notopen:
            print("=> ALERT MISMATCH!!! Sending out alerts ...")
            send_emails_notif("stockholm")
            update_status("stockholm", num_boxes, num_notopen, db, cursor)
        else:
            print("=> no mismatch, no change ...")
            

        browser.quit()
        # sleepy time
        print("=> Sleepy time for {} seconds... zzzzz".format(sleep_time))
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
