#
# Basic web scraper–– Retrieves list of 100 companies with the highest market
# cap, scrapes prices individually.
# 
# Requires bs4 and selenium
# 
# @author Josh Smith
#

from bs4 import BeautifulSoup
from selenium import webdriver
import time

stocks_to_find = []
success = 0
total = 0

print("Running Company Market Cap Scraper")

# Initialize browser tool

driver = webdriver.Chrome()

# Scrape top 100 companies from companiesmarketcap.com

print("Collecting company list")

driver.get("https://companiesmarketcap.com/")

time.sleep(3)

html = driver.page_source

soup = BeautifulSoup(html, features="html.parser")

for tag in soup.find_all(class_='company-name'):
    stocks_to_find.append(tag.text.replace("&", "and"))

#print(stocks_to_find)
total_entries = len(stocks_to_find)

# Parse stock list–– search price by class from bing homepage

print("Collecting stock data: " + str(total_entries) + " entries total.")

for stock in stocks_to_find:
    
    try:
        driver.get('https://www.bing.com/search?q=' + stock + ' stock')

        html = driver.page_source

        soup = BeautifulSoup(html, features="html.parser")

        for tag in soup.find(class_='b_focusTextMedium'):
            print("(" + str(total + 1) + "/" + str(total_entries) + ") " + stock.capitalize() + ": " + tag.text)
            success += 1

    except:
        print(stock.capitalize() + ": Error retrieving price")
    
    total += 1

# Print success rate (for debugging)
print("Query success rate: " + str(success) + "/" + str(total) + " (" + str(success / total * 100)  + " %)")
