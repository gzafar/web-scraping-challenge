from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import requests

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)



















