
# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import tweepy
import time
import pandas as pd
from selenium import webdriver

# Scrape Function

def scrape():
    final_mars_data = {}
    final_mars_data['mars_news'] = get_latest_NASA_news()
    final_mars_data['mars_image'] = get_MARS_img()
    final_mars_data['mars_temp'] = get_MARS_temperature()
    final_mars_data['mars_facts'] = get_MARS_facts()
    final_mars_data['mars_hm_data'] = get_MARS_hemisphere_data()
    
    return final_mars_data

#NASA Mars News 

def get_latest_NASA_news():
        driver = webdriver.Chrome('C:/Users/victo/ChromeDriver/chromedriver.exe') 
        mars_news = 'https://mars.nasa.gov/news/'
        driver.get(mars_news)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        news_title = soup.find("div", class_ = "content_title").text
        news_content = soup.find("div", class_ = "article_teaser_body").text
        news = [news_title, news_content]
        #print(news)
        driver.quit()
        return news 


def get_MARS_img():
        driver = webdriver.Chrome('C:/Users/victo/ChromeDriver/chromedriver.exe') 
        mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        driver.get(mars_image)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find("a", class_ = "button fancybox")
        featured_image_url = mars_image + images.get('data-fancybox-href')
        #print(featured_image_url)
        driver.quit()
        return featured_image_url 


def get_MARS_temperature():
        driver = webdriver.Chrome('C:/Users/victo/ChromeDriver/chromedriver.exe') 
        twitter_url = "https://twitter.com/marswxreport?lang=en"
        html = driver.page_source
        response = requests.get(twitter_url)
        soup = BeautifulSoup(response.text,"lxml")
        tweets = soup.findAll('li',{"class":'js-stream-item'})
        tweet_records = []
        for tweet in tweets:
                if tweet.find('p',{"class":'tweet-text'}):
                        tweet_text = tweet.find('p',{"class":'tweet-text'}).text.encode('utf8').strip()
                        tweet_records.append(tweet_text)
        mars_weather_status = tweet_records[1]
        #print(mars_weather_status)
        driver.quit()
        return mars_weather_status



def get_MARS_facts():
        driver = webdriver.Chrome('C:/Users/victo/ChromeDriver/chromedriver.exe') 
        facts = requests.get("https://space-facts.com/mars/")
        soup = BeautifulSoup(facts.content, 'lxml')
        mars_table = soup.find_all('table')[0]
        mars_data = pd.read_html(str(mars_table))[0]
        mars_data.columns = ["Description", "Value"]
        mars_data = mars_data.set_index("Description")
        mars_facts = mars_data.to_html(index = True, header =True)
        #print(mars_facts)
        driver.quit()
        return mars_facts


def get_MARS_hemisphere_data():
        driver = webdriver.Chrome('C:/Users/victo/ChromeDriver/chromedriver.exe') 
        hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        driver.get(hemisphere_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        mars_hemisphere_list = []

        products = soup.find("div", class_ = "result-list" )
        hemispheres = products.find_all("div", class_="item")

        for hemisphere in hemispheres:
                title = hemisphere.find("h3").text
                title = title.replace("Enhanced", "")
                end_link = hemisphere.find("a")["href"]
                image_url = "https://astrogeology.usgs.gov/" + end_link
                mars_hemisphere_list.append({"title": title, "img_url": image_url})
        def get_high_res_url(some_url):
                response = requests.get(some_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all("a")
                tifs = [j for j in links if ".tif" in j.attrs.get('href')]
                return tifs[0].get('href')

        updated_photos = []

        for data in mars_hemisphere_list:
                link_to_check = data.get('img_url')
                title = data.get('title')
                final_image_url = get_high_res_url(link_to_check)
                updated_photos.append({
                'Title': title,
                'Url': final_image_url
                })

        #print(final_image_url)
        driver.quit()
        return updated_photos

