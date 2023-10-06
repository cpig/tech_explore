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
BEGIN = 345

driver=webdriver.Firefox()
driver.set_page_load_timeout(15)

fin = open("ikea_category_top_item.tsv", "r", encoding="utf8")
fout = open("ikea_ranking_pages.tsv","a",encoding="utf8")

def get_tag_info(url):
    try:
        driver.get(url)
    except:
        pass
    bs4_page = BeautifulSoup(driver.page_source,"html.parser")
    ranking_tag = bs4_page.find("a",{"class":"ranking-tag"})
    ranking_link = ranking_tag["href"]
    ranking_tag_name = ranking_tag.find("div",{"class":"ranking-tag-name"}).text.strip()
    return ranking_link, ranking_tag_name
    

line_cnt = 0
for i in range(BEGIN):
    fin.readline()
for line in fin:
    line_split = line.strip().split('\t')
    category_title = line_split[0]
    top_items = line_split[1:]
    for item_link in top_items:
        try:
            ranking_link, ranking_tag_name = get_tag_info(HOST + item_link)
            break
        except:
            print("Failed in reading " + item_link)
            pass
    if ranking_link:
        fout.write("\t".join([category_title, ranking_link, ranking_tag_name])+"\n")
    else:
        fout.write(category_title + "\t" + "FAIL" + "\n")
    line_cnt+=1
    print(line_cnt)
fout.close()
