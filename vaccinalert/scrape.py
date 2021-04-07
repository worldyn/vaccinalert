import requests 
#from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#browser = webdriver.Chrome("./chromedriver")
browser = webdriver.PhantomJS()
url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
browser.get(url)

print("\n\n=> Scraping 1177.se")
#print(browser.title)

boxes = browser.find_elements_by_css_selector(".c-teaser-outer .c-image img")

#with open("1177.html", "w") as f:
#    f.write(browser.page_source)

num_boxes = len(boxes)
print("=> Number of boxes: ", num_boxes)

for i,box in enumerate(boxes):
    print("IMG SRC: ", box.get_attribute("src"))


browser.quit()
