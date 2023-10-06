import urllib
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

driver=webdriver.Firefox()
driver.get(HOST + "/cn/zh/room-ranking/all/")
#time.sleep(5)

bs4Page=BeautifulSoup(driver.page_source,"html.parser")
card_list=bs4Page.findAll("div",{"class":"category-ranking-card"})

fout = open("ikea_category_top.tsv","w",encoding="utf8")

for card in card_list:
    card_title = card.find("p",{"class":"head__title"}).text
    fout.write(card_title)
    item_list = card.findAll("a",{"class":"category-ranking-card__product"})
    for item in item_list:
        item_link = item["href"]
        fout.write("\t" + item_link)
fout.write("\n")
