# This tool collects the market type of LSE listed companies from the LSE website, something that can't be easily downloaded
# For example, on the website for Domino's: https://www.londonstockexchange.com/stock/DOM/domino-s-pizza-group-plc/company-page
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

#### routine for detecting small cap firms
response = requests.get("https://www.sharecast.com/index/FTSE_Small_Cap")
soup = BeautifulSoup(response.text, 'lxml')
market_cap = soup.find_all("td", class_="text-right xs-col-2 nth-order-5 capitalization-ttl")

sc_firms_marketcap = []

for i in market_cap:
    entry = i.get_text().replace('\n','').replace('£','').replace('m','').strip()
    sc_firms_marketcap.append(float(entry))

largest_firm_cap = max(sc_firms_marketcap)

# this webpage isn't as reliable as the previous so a try/except is used here
try:
    response = requests.get("https://www.sharecast.com/index/FTSE_Small_Cap/market-capitalization/desc")
    soup = BeautifulSoup(response.text, 'lxml')
    company_names = soup.find_all("th", class_="xs-col-3 nth-order-1 ttl")
    top_sc_firm_name = company_names[0].get_text().replace('\n','').strip()
    top_sc_firm_name
except:
    top_sc_firm_name = "*NOT FOUND*"
    pass

print(f"Script finds largest SmallCap firm is *{top_sc_firm_name}* at £{largest_firm_cap}m")
####

print("\nScript now searching for firms on LSE website...") 

search_error_counter = 0

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
    time.sleep(0.5) # half second for all the elements to load; testing shows the script doesn't work without it
    try:
        gdpr = driver.find_elements_by_id("ccc-notify-accept")
        gdpr[0].click()
    except: # if it can't open a link, it will retry 5 times before acquiescing
        for i in range(5):
            try:
                time.sleep(0.5)
                gdpr[0].click()
                break
            except:
                found = False
                pass
   
        
    # goes through the search results and finds links with the company name in it, clicking on the first result
    search = driver.find_elements_by_xpath('//*[contains(text(), " {} ")]'.format(company_name))    
    time.sleep(0.5)
    try: # if the company cannot be found then it is recorded as so, then passing on to the next company
        search[0].click()
    except:
        for i in range(5):
            try:
                time.sleep(0.5)
                search[0].click()
                break
            except:
                found = False
                pass
    
    if found == True: # if it finds the company's page then it records the url
        url.append(driver.current_url)
    elif found == False:
        url.append("https://www.blank.org/") # if it can't find it then it records a blank website 
        
                                   
    # sometimes a valid company gets caught on the search page, in which case this makes it retry
    if driver.current_url[37] == "e" and search_error_counter < 3: # this is a characteristic of the search page, part of forcing it to retry
        print(f"Error finding *{company_name}*, retrying {search_error_counter+1}/3 attempts")
        search_error_counter += 1
        url.pop()
        found = True
        driver.close()
        continue
    else:
        a += 1
        
    found = True    
    print(f"Found firm {a}/{len(col)}")
    driver.close()
    search_error_counter = 0

print("\n")
print("\nFirms LSE website pages identified")    
print("\nThe URLs for the companies on the LSE website were:")
for a in url:
    if a == "https://www.blank.org/":
        print("*NOT FOUND*")
    else:
        print(a)

print("\nNow determining market types...")


### this routine verifies that a detected smallcap firm is indeed found on the index or not
# using the official LSE index, not used elsewhere because it doesn't store the market caps
SC_index = ["https://www.hl.co.uk/shares/stock-market-summary/ftse-small-cap?page=1",
            "https://www.hl.co.uk/shares/stock-market-summary/ftse-small-cap?page=2",
            "https://www.hl.co.uk/shares/stock-market-summary/ftse-small-cap?page=3"]
smallcap_firm_list = []

for l in SC_index:
    response = requests.get(l)
    soup = BeautifulSoup(response.text, 'lxml')
    firm_name = soup.find_all("td", class_="name-col align-left")

    for m in firm_name:
        smallcap_firm_list.append(m.get_text().lower())
###


# this section detects which companies are listed as AIM or Main Market, now their URLs are collected
book = []
record = []
counter = 0

        
for j in url:
    
    for k in range(6): # five attempts of getting the market type before giving up
        book = []
        response = requests.get(j)
        soup = BeautifulSoup(response.text, 'lxml')
        market_type = soup.find_all("app-index-item", class_="index-item")
        
        for i in market_type:
            book.append(i.text)
            
        if j == "https://www.blank.org/":
            record.append("Company not found on LSE website")
            break
            
        elif " Market Main Market" in book:
            collection = soup.find_all("div", class_="bold-font-weight regular-font-size")
            company_mc = float(collection[5].getText().replace(',',''))
            
            if company_mc <= largest_firm_cap:
                # this gets the name of the current firm from the URL and checks if it's in the list of SC firms
                potential_smallcap = j.replace("/company-page",'')
                potential_smallcap = potential_smallcap.split('/')
                potential_smallcap = potential_smallcap[5]
                potential_smallcap = potential_smallcap.replace('-',' ').lower()
                
                if potential_smallcap in smallcap_firm_list:
                    record.append("SmallCap")
                else:
                    record.append("SmallCap size but couldn't find in SmallCap index")
            else:
                record.append("Main Market")
            break
            
        elif " Market AIM" in  book:
            record.append("AIM")
            break
            
        elif k == 5:
            record.append("Company in LSE website but market not found")
        print(f"Company {counter} not found, {k}/5 attempts")
        
    counter += 1
    print(f"Found {counter}/{len(col)} market types")

print(record)
df = pd.DataFrame(record)
df.to_excel("output_file.xlsx")

print("\n")
print("\nScript complete!")
