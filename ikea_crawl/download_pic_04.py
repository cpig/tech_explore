import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import random
import sys
import os
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

HOST = "https://www.ikea.cn"


fin = open("ikea_top_item_sales.tsv", "r", encoding="utf8")

down_cnt=0
read_cnt=0
for line in fin:
    read_cnt+=1
    try:
        pic_url = line.split('\t')[3]
    except:
        print("Error line: " + line.strip())
    pic_file_name = pic_url.split('/')[-1]
    if pic_file_name in os.listdir('pic'):
        continue
    urllib.request.urlretrieve(pic_url,"pic\\"+pic_file_name)
    down_cnt+=1
    print("down:", down_cnt, "  read:", read_cnt)
    

    
