#import ssl -- needed this for MAC
import csv #used to put List into CSV
from urllib.request import urlopen as uReq #using this to open the URL
from bs4 import BeautifulSoup as soup #using BeautifulSoup to parse through the HTML

#needed to import ssl for MAC
#ssl._create_default_https_context = ssl._create_unverified_context

#Accessing the Walmart below
my_url = "https://www.walmart.com/search/?query=lysol%20disinfectant%20spray&cat_id=1115193&typeahead=lysol%20dis"

#Storing the urlopen or ureq in uClient
#Then using .read() to read the HTML
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#using BeautifulSoup to parse the HTML
page_soup = soup(page_html, "html.parser")

#Creating arrays that will house the products, that are in stock and out of stock
out_of_stock=[]
in_stock_in_store =[]
in_stock_delivery =[]

#Using the below to pull in the div that holds the items regardless being in stock for in store purchase or out of stock
conclass = page_soup.findAll("div",{"class": "search-result-gridview-item clearfix arrange-fill"})

#Using outter foor loop to go through all the divs and using range to set container as an Int to traverse the conclass[x] list
for container in range(0,len(conclass)):
    #First If condition is to see if the div is a span checking if the title is Out of Stock
    if (conclass[container].find("span","ppu-out-of-stock")):

        conclass_container = conclass[container]
        product = conclass_container.findAll("a", {"class": "product-title-link line-clamp line-clamp-2 truncate-title"})

        #Second for loop is to go through the index of container, which is stored in Product and pulling the text out of that, and encoding it to UTF-8, this repeats for both the in-stock
        #conditions below as well.
        for each in product:

            out_of_stock.append((each.text.strip().encode('utf-8')))

    elif conclass[container].find("div",{"class": "product-sub-title-block product-in-store-only"}):
        conclass_container = conclass[container]
        product = conclass_container.findAll("a", {"class": "product-title-link line-clamp line-clamp-2 truncate-title"})
        for each in product:

            in_stock_in_store.append((each.text.strip().encode('utf-8')))
    elif conclass[container].find("div",{"class": "ShippingMessage-container color-black"}):
        conclass_container = conclass[container]
        product = conclass_container.findAll("a", {"class": "product-title-link line-clamp line-clamp-2 truncate-title"})
        for each in product:

            in_stock_delivery.append((each.text.strip().encode('utf-8')))


#Creating a CSV file for each of the Lists and writing the values in the first row

with open('OutofStock.csv', 'w') as OutofStock:
    wr = csv.writer(OutofStock, quoting=csv.QUOTE_ALL)
    wr.writerow(out_of_stock)

with open('InStockinStore.csv', 'w') as InStockInStore:
    wr = csv.writer(InStockInStore, quoting=csv.QUOTE_ALL)
    wr.writerow(in_stock_in_store)

with open('InStockDelivery.csv', 'w') as InStockDelivery:
    wr = csv.writer(InStockDelivery, quoting=csv.QUOTE_ALL)
    wr.writerow(in_stock_delivery)




