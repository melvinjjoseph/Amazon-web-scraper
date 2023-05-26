from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from time import sleep
import re

if __name__ == '__main__':
    #headers for request
    HEADERS = ({'User-Agent':'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'Accept-Language': 'en-US, en;q=0.5'})
    #url of the page to be scraped
    URL="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data in an amazon page
    soup = BeautifulSoup(webpage.content, "html.parser")
    # Fetch links as List of Tag Objects of all the search results
    comp=soup.find_all("div", attrs={'data-component-type':'s-search-result'})

    #initialize an empty list to store the links
    links_list = []
    #loop for extracting data from Tag Objects 
    for i in comp:
        link = i.find("a", attrs={'class':'a-link-normal s-no-outline'})
        url="https://www.amazon.in" + link.get('href')
        links_list.append(url)

    # Creating a dictionary having the features as keys
    d={"url":[], "title":[], "price":[], "rating":[], "reviews count":[], "asin":[],"description":[], }
    for url in links_list:
        webpage = requests.get(url, headers=HEADERS)
        d["url"].append(url)
        soup=BeautifulSoup(webpage.content,"html.parser")
        try:
            title=soup.find("span", attrs={'id':'productTitle'}).text.strip()
        except AttributeError:
            title = ''
        d["title"].append(title)

        try:
            price=soup.find("span", attrs={"class":"a-price-whole"}).text.strip()
        except AttributeError:
            price = ''
        d["price"].append(price)
        try:
            rating=soup.find("span", attrs={'class':'a-icon-alt'}).text.strip()
        except AttributeError:
            rating = ''
        d["rating"].append(rating)
        try:
            reviews=soup.find("span", attrs={'id':'acrCustomerReviewText'}).text.strip()
        except AttributeError:
            reviews = ''
        d["reviews count"].append(reviews)
        try:
            description=soup.find("div", attrs={'id':'feature-bullets'}).text.strip()
        except AttributeError:
            description = ''
        d["description"].append(description)
        asin = re.search(r"/[dg]p/([^/]+)", url, flags=re.IGNORECASE)
        if asin:
            d["asin"].append(asin.group(1))
                # print(d)
        sleep(2)

    print(d)
    
    # Converting the dictionary into a pandas dataframe
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])

    #saving the dataframe to a csv file
    amazon_df.to_csv("amazon_data2.csv", header=True, index=False)
    print("Data saved to csv file")

