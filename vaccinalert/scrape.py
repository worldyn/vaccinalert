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


        errorTries = 0



        # setup web browser
        warnings.simplefilter("ignore")
        browser = webdriver.PhantomJS()
        browser_two = webdriver.PhantomJS() # new code 7/7

        # sthlm hardcoded
        url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
        url_two = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/nar-och-hur-kan-jag-vaccinera-mig-mot-covid-19/'
        #url = 'https://www.1177.se/'
        browser.get(url)

        # new code 7/7
        browser_two.get(url_two)


        boxes = browser.find_elements_by_css_selector(".c-teaser-outer .c-image img")

        # GH: get boxes teaser text
        boxes_content = browser.find_elements_by_css_selector(".c-teaser__text")
        
        # new code 
        boxes = browser.find_elements_by_css_selector(".c-teaser-outer .c-image img")

        num_boxes = len(boxes)
        #print("=> Number of boxes: ", num_boxes)

        not_open = "annu-inte-oppen" # hardcoded stuff sthlm
        num_notopen = 0



        for i,box in enumerate(boxes):
            imgsrc = box.get_attribute("src")
            if not_open in imgsrc:
                num_notopen += 1
        
        #print("=> Number of closed boxes: ", num_notopen)



        # GH: new code
    
        search_failed = False

        try:
            info_text = browser_two.find_element_by_id('section-126101').find_element_by_tag_name('div').find_element_by_tag_name('p')
        except:
            search_failed = True

        print("=> Search failed?: {}".format(search_failed))



        '''

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
        
        '''


        #print("=> scraped box {}, scrape closed {}".format(num_boxes, num_notopen))

        # GH: important change!
        #if num_boxes >= num_notopen and num_notopen != 0 and num_boxes != 0:
        #if num_boxes >= num_notopen and num_boxes != 0:
        if search_failed == False:

            # GH: getting the age
            box_current_age = int(max(re.findall(r'(\d{4,4})', info_text.get_attribute('textContent'))))

            print("=> Checking db status...")

            try:

                '''
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
                '''
                

                # GH: get age box aswell
                db, cursor = connect()
                curr_num_age_from_db = get_status_age("stockholm", db,cursor)

                print("=> Database retrieval successful")

                # GH: if mismatch send out emails and update db
                if box_current_age > curr_num_age_from_db:
                    print("=> ALERT MISMATCH!!! Sending out alerts ...")

                    send_emails_notif("stockholm")

                    update_status_age("stockholm", box_current_age, db, cursor)

                errorTries = 0
                print ("ERROR TRIES in success scrape: ", errorTries)
                
            except:
                print("ERROR Database / could not reach...")
                # send mail to support! 
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
                send_support(timestamp, " Database error, check log ") 
    
        
        elif errorTries < 15:
            errorTries += 1
            print ("ERROR TRIES: ", errorTries)

        else:
            #print("ERROR scraping, num boxes {}, num closed {}".format(num_boxes, num_notopen))
            print("ERROR scraping, age not found")
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
