from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

stocks_to_find = []
success = 0
total = 0

print("Running Company Market Cap Scraper")

options = Options()
#options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

print("Collecting company list")

driver.get("https://companiesmarketcap.com/")

time.sleep(10)

html = driver.page_source

soup = BeautifulSoup(html, features="html.parser")

for tag in soup.find_all(class_='company-name'):
    stocks_to_find.append(tag.text)

#print(stocks_to_find)
total_entries = len(stocks_to_find)

print("Collecting stock data: " + str(total_entries) + " entries total.")

for stock in stocks_to_find:
    
    try:
        driver.get('https://duckduckgo.com/?t=h_&q=' + stock + " stock")

        html = driver.page_source

        soup = BeautifulSoup(html, features="html.parser")

        for tag in soup.find(class_='stocks-module__currentPrice'):
            print("(" + str(total + 1) + "/" + str(total_entries) + ") " + stock.capitalize() + ": " + tag.text)
            success += 1

    except:
        print(stock.capitalize() + ": Error retrieving price")
    
    total += 1

print("Query success rate: " + str(success) + "/" + str(total) + " (" + str(success / total * 100)  + " %)")
