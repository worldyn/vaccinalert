import requests 
#from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import time
from dbutils import *
from emailsender import *
import random
import warnings
from datetime import datetime
import re

def main():
    sleep_time = 100 # seconds
    print("=> script.py started ...")

    while True:
        #print("\n\n")
        #print("=> Scraping 1177.se")

        # setup web browser
        warnings.simplefilter("ignore")
        browser = webdriver.PhantomJS()
        # sthlm hardcoded
        url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
        #url = 'https://www.1177.se/'
        browser.get(url)

        boxes = browser.find_elements_by_css_selector(".c-teaser-outer .c-image img")



        # GH: get boxes teaser text
        boxes_content = browser.find_elements_by_css_selector(".c-teaser__text")


        num_boxes = len(boxes)
        print("=> Number of boxes: ", num_boxes)

        not_open = "annu-inte-oppen" # hardcoded stuff sthlm
        num_notopen = 0



        for i,box in enumerate(boxes):
            imgsrc = box.get_attribute("src")
            if not_open in imgsrc:
                num_notopen += 1
        
        print("=> Number of closed boxes: ", num_notopen)


        # GH: checks for the biggest number in the boxes content text
        #box_current_age = int(''.join(re.findall(r'(\d{4,4})', boxes_content[0].get_attribute("textContent"))))
        box_current_age = []
        list_with_ages = []
        
        if (len(boxes_content) != 0):
            for i,box in enumerate(boxes_content):
                box_current_age.append(re.findall(r'(\d{4,4})', boxes_content[i].get_attribute("textContent")))

            for e in box_current_age:
                for l in e:
                    list_with_ages.append(int(l))

            box_current_age = max(list_with_ages)


        # test value if needed
        #box_current_age = 1980
        print("=> scraped box with phase 4 age {}".format(box_current_age))
        
    

        print("=> scraped box {}, scrape closed {}".format(num_boxes, num_notopen))

        # GH: important change!
        #if num_boxes >= num_notopen and num_notopen != 0 and num_boxes != 0:
        if num_boxes >= num_notopen and num_boxes != 0:
            #print("=> Checking db status...")
            try:
                db, cursor = connect()
                curr_num_groups, curr_num_closed_groups = get_status("stockholm", db,cursor)
                print("=>scraped box {}, scrape closed {}, curr #groups {}, curr # closed groups {}".format(num_boxes, num_notopen,curr_num_groups, curr_num_closed_groups))

                # GH: get age box aswell
                curr_num_age_from_db = get_status_age("stockholm", db,cursor)

                # if mismatch send out emails and update db
                if curr_num_groups >= curr_num_closed_groups and type(curr_num_groups) == int and type(curr_num_closed_groups) == int and curr_num_closed_groups > num_notopen:
                    print("=> ALERT MISMATCH!!! Sending out alerts ...")

                    
                    send_emails_notif("stockholm")

                    update_status("stockholm", num_boxes, num_notopen, db, cursor)

                # GH: if mismatch send out emails and update db
                if box_current_age > curr_num_age_from_db:
                    print("=> ALERT MISMATCH!!! Sending out alerts ...")

                    send_emails_notif("stockholm")

                    update_status_age("stockholm", box_current_age, db, cursor)

            except:
                print("ERROR Database / could not reach...")
                # send mail to support! 
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
                send_support(timestamp, " Database error, check log ") 
        
        
        else:
            print("ERROR scraping, num boxes {}, num closed {}".format(num_boxes, num_notopen))
            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
            send_support(timestamp, " Error scraping 1177, check log ") 
        



        browser.quit()
        # sleepy time
        sleep = sleep_time + random.randrange(15) 
        print("=> Sleepy time for {} seconds... zzzzz".format(sleep))
        time.sleep(sleep)
        

if __name__ == "__main__":
    main()
