import requests 
#from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#browser = webdriver.Chrome("./chromedriver")
browser = webdriver.PhantomJS()
url = 'https://www.1177.se/Stockholm/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/om-vaccin-mot-covid-19/boka-tid-for-vaccination-mot-covid-19-i-stockholms-lan/'
browser.get(url)

print("=> \n\nScraping 1177.se")
#print(browser.title)
boxes = browser.find_elements_by_class_name("c-teaser-outer")
#with open("1177.html", "w") as f:
#    f.write(browser.page_source)
print("=> Number of boxes: ", len(boxes))

browser.quit()



#response = requests.get(url) #Getting the response from mentioned URL using get() method of requests 
#html = response.content
#soup = BeautifulSoup(html)  
#print(soup)

'''
table = soup.find('table', attrs={'id': 'example2'}) #From BeautifulSoup of HTML content, finding the tbody(data of table) of the desired table having specific attributes, here desired table has 'example2' as idtbody = table.find('tbody')
list_of_rows = []
for row in tbody.findAll('tr')[0:]:  #line 11-16, Traversing every row('tr') and every cell of a row ('td') in table and making list of rows    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace(' ', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)
'''
