from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import requests
from flask import Flask, render_template
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

def scrape():
    browser=init_browser()
    mars_dict = {}

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # NASA Mars News
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL Mars Space Images - Featured
    space_images_url = 'https://spaceimages-mars.com/'
    browser.visit(space_images_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_url = soup.find('img', class_='headerimage fade-in')['src']

    featured_img_url = space_images_url+image_url

    # Mars Facts
    mars_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_url)

    table = pd.read_html(mars_url)
    df = table[0]

    html_table = df.to_html('table.html')

    # Mars Hemispheres
    mars_hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemispheres_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = soup.find('div', class_='collapsible results')

    mars_hemispheres = hemispheres.find_all('div', class_='item')
    mars_hemispheres = []

    for hemisphere in mars_hemispheres:
        img_desc = hemisphere.find('div', class_='description')
        title = hemisphere.h3.text

        hemisphere_url = img_desc.a['href']
        
        browser.visit(mars_hemispheres_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_src = soup.find('img', class_='thumb')['src']
        
        if(title and img_src):
            print(title)
            print(mars_hemispheres_url + img_src)
            
        hemisphere_dict = {
            'title': title,
            'img_src': img_src
        }
        
    mars_hemispheres.append(hemisphere_dict)



    mars_dict = {
    'news_title': news_title,
    'news_p': news_p,
    'featured_img_url': featured_img_url,
    'html_table': html_table,
    'mars_hemispheres': mars_hemispheres
    }   

    mars_dict

    browser.quit()

    return mars_dict












