
#Dependencies

from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
import pandas as pd

# setup mongo connection

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=False)
    return browser


def mars_news_scrape():
# URL of page to be scraped
    browser = init_browser()
    url='https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')


        # ## Nasa Mars News
        #Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    results = soup.find_all('div', class_='list_text')
    
        # Loop through returned results
    mars_news= []
    for result in results:
            # Error handling

                # Identify and return title of listing
        news_title = result.find('div', class_='content_title')
                # Identify and return paragraph of listing
        news_paragraph = result.find('div', class_='article_teaser_body')
        marsNews=dict({'title':news_title, 'paragraph':news_paragraph})
        mars_news.append(marsNews)    
                # Print results only if title, price, and link are available
        if ( news_title and news_paragraph):
                    print('-------------')
                    print(news_title)
                    print(news_paragraph)

        return mars_news

# ## JPL Mars Space Images-Featured Image
#use splinter to navigate the site and find the image url for the current Featured Mars Image 
#and assign the url string to a variable called featured_image_url

def img_scrape():
    browser = init_browser()
    url='https://spaceimages-mars.com/'

    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    #Scrape the spaceimages-mars Site and collect the images
    images = soup.find_all('a', class_='fancybox-thumbs')
    images

    # Loop through returned results
    featured_image_url_list=[]
    for img in images:
        # Error handling
            # Identify and return image href
        featured_url = img['href']
        featured_image_url='https://spaceimages-mars.com/'+ f'{featured_url}'
        featured_img=dict({'img_url':'https://spaceimages-mars.com/'+ f'{featured_url}'})
        featured_image_url_list.append(featured_img)
        if ( featured_image_url,featured_image_url):
            print('-------------')    
            print(featured_image_url)
           # print(featured_image_url_list)
    return featured_image_url_list


# ## Mars Facts

#Visit the Mars Facts webpage and use Pandas to scrape the table containing facts
#about the planet including Diameter, Mass, etc.

#Use Pandas to convert the data to a HTML table string
def mars_facts():

    url='https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)
    tables
    type(tables)

    df = tables[0]
    df.head()

    #Remove top header
    New_df=df.rename(columns=df.iloc[0]).drop(df.index[0])
    #Reset an Index and keep old column
    New_df=New_df.rename(columns={'Mars - Earth Comparison':'Description'})
    New_df=New_df.set_index('Description')
    New_df

    
    # ### DataFrame as HTML


    html_table = New_df.to_html()
    html_table
    html_table.replace('\n', '')

    New_df.to_html('table.html')
    mars_data = New_df.to_html()
    
    get_ipython().system('open table')

    return mars_data
# ## Mars Hemispheres

#executable_path={'executable_path': ChromeDriverManager().install()}
#browser=Browser('chrome', **executable_path, headless=False)


#Visit the astrogeology site to obtain high resolution images for each 
#of Mar's hemispheres.
def marshemispheres():

    browser = init_browser()
    url='https://marshemispheres.com/'


    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    images = soup.find_all('div', class_='item')
    images

    # Loop through returned results

    hemisphere_img_urls =[]

    for img in images:
        # Error handling
            # Identify and return image href
            div=img.find('div')
            title=div.find('h3').text
            link=div.find('a')
            img_url = link['href']
            image_url='https://marshemispheres.com/'+ f'{img_url}'
            img_data=dict({'title':title, 'img_url':image_url})
            #append dictionary to hemisphere_img_urls list
            hemisphere_img_urls.append(img_data)
            if (title, image_url, hemisphere_img_urls):
                print('-------------')  
                print(title)
                print(image_url)
                print(hemisphere_img_urls)    

    browser.quit()
    return image_url















