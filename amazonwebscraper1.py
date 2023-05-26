from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from time import sleep

if __name__ == '__main__':

    HEADERS = ({'User-Agent':'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'Accept-Language': 'en-US, en;q=0.5'})
    links_list = []
    titles_list = []
    prices_list = []
    ratings_list = []
    reviews_list = []
    
    #loop for extracting data from 20 pages
    for i in range(1,21):
        URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
        URL = URL + str(i)

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data in an amazon page
        soup = BeautifulSoup(webpage.content, "html.parser")
        # Fetch links as List of Tag Objects of all the search results
        comp=soup.find_all("div", attrs={'data-component-type':'s-search-result'})
        
        #loop for extracting data from Tag Objects
        for i in comp:
            link = i.find("a", attrs={'class':'a-link-normal s-no-outline'})
            url="https://www.amazon.in" + link.get('href')
            links_list.append(url)
            title = i.find("span", attrs={'class':'a-size-medium a-color-base a-text-normal'}).text.strip()
            titles_list.append(title)
            price= i.find("span", attrs={'class':'a-price-whole'}).text.strip()
            prices_list.append(price)
            rating= i.find("span", attrs={'class':'a-icon-alt'}).text.strip()
            ratings_list.append(rating)
            reviews= i.find("span", attrs={'class':'a-size-base s-underline-text'}).text.strip()
            reviews_list.append(reviews)

    # Creating a dictionary having the features as keys
    d = {"url":links_list,"title":titles_list, "price":prices_list, "rating":ratings_list, "reviews count":reviews_list}

    # Converting dictionary to Pandas Dataframe
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)