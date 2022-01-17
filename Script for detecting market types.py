# This tool collects the market type of LSE listed companies from the LSE website, something that can't be easily downloaded
# For example, on the page for Domino's pizza group PLC: https://www.londonstockexchange.com/stock/DOM/domino-s-pizza-group-plc/company-page
# Under 'Instrument information' it is recorded as 'Main Market'

import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = []

found = True

df = pd.read_excel("input.xlsx")

col = df["Company Name"].tolist()

a = 0

while a < len(col): # iterates through the companies the user uploaded

    company_name = col[a]

    company_name = company_name.upper() # LSE company site has companies in capitals, so user companies are capitalised so it knows what to look for 
    
    # searches for the company in the search bar (or rather mimics the url that would be produced in searching to save time)
    address = "https://www.londonstockexchange.com/search?searchtype=all&q=" + company_name.replace(" ","%20") # likewise, company names in the url have dashes for spaces

    
    # opens chrome and searches for the above url
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(address)

    
    # clicks accept on the automatic GDPR notice 
    time.sleep(1) # one second for all the elements to load; script doesn't work without it
    gdpr = driver.find_elements_by_id("ccc-notify-accept")
    gdpr[0].click()

    
    # goes through the search results and finds links with the company name in it, clicking on the first result
    search = driver.find_elements_by_xpath('//*[contains(text(), " {} ")]'.format(company_name))    
    time.sleep(1)
    try: # if the company cannot be found then it is recorded as so, then passing on to the next company
        search[0].click()
    except IndexError:
        found = False
        pass
    
    if found == True: # if it finds the company's page then it records the url
        url.append(driver.current_url)
    elif found == False:
        url.append("https://www.blank.org/") # if it can't find it then it records a blank website 
    
    found = True
    
    driver.close()
    
    a += 1

# this section detects which companies are listed as AIM or Main Market, now their URLs are collected
book = []
record = []

for j in url:
    response = requests.get(j)
    soup = BeautifulSoup(response.text, 'lxml')
    market_type = soup.find_all("app-index-item", class_="index-item")
    
    for i in market_type:
        book.append(i.text)
    if j == "https://www.blank.org/":
        record.append("Company not found on LSE website")
    elif " Market Main Market" in book:
        record.append("Main Market")
    elif " Market AIM" in  book:
        record.append("AIM")
    else:
        record.append("Company in LSE website but market not found")
    book = []

print(record)
df = pd.DataFrame(record)      
df.to_excel("output_file.xlsx")

