import urllib
from bs4 import BeautifulSoup
import codecs
import time
import random
import sys
import os
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

PicWorkId=sys.argv[1]
driver=webdriver.Firefox()
driver.get("http://www.cnu.cc/works/"+PicWorkId)
#time.sleep(5)

bs4Page=BeautifulSoup(driver.page_source,"html.parser")
imgList=bs4Page.findAll("img",{"class":"bodyImg"})

if not os.path.exists("CNU_"+PicWorkId):
    os.mkdir("CNU_"+PicWorkId)
for img in imgList:
    path=img["data-original"]
    urllib.request.urlretrieve(path,"CNU_"+PicWorkId+"\\"+path.split('/')[-1])
driver.close()
