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
BEGIN = 0

driver=webdriver.Firefox()
driver.set_page_load_timeout(15)

fin = open("ikea_ranking_pages.tsv", "r", encoding="utf8")
fout = open("ikea_top_item_sales.tsv","w",encoding="utf8")

def get_items_info(url):
    result = []
    try:
        driver.get(url)
    except:
        pass
    try_cnt = 0
    while try_cnt <=5:
        if try_cnt>0:
            print("   try:" +str(try_cnt) )
        time.sleep(0.5)
        bs4_page = BeautifulSoup(driver.page_source,"html.parser")
        top_items = bs4_page.findAll("div",{"class":"ranking-main-product"})

        try:
            for item in top_items:
                title = item.find("p", {"class":"product-name"}).text.strip()
                subtitle = item.find("p", {"class":"product-specification"}).text.strip()
                link = item.find("a",{"class":"product-link"})["href"]
                pic = item.find("a",{"class":"landscape-product-card__image"}).find("img")["src"]
                try:
                    quantity = int(item.find("p",{"class":"product-ranking-description"}).text.strip()[4:-1])
                except:
                    continue
                price = float(item.find("span",{"class":"withprice-price"}).text.strip().replace(",","")+\
                         item.findAll("span",{"class":"withprice-symbol"})[1].text.strip())
                #link = item.find("div",{"class":"price"})#.text
                #print(link.text)
                result.append([title, subtitle, link, pic, str(quantity), str(price)])
            break
        except Exception as e:
            print("Error in parsing " + url + " " + repr(e))
            try_cnt += 1
            result = []
            continue
            
    return result
    

line_cnt = 0
for i in range(BEGIN):
    fin.readline()
for line in fin:
    line_cnt+=1
    line_split = line.strip().split('\t')
    if len(line_split)!=3:
        continue
    category_title = line_split[0]
    rank_link = line_split[1]
    top_item_list = get_items_info(HOST+rank_link)
    for item in top_item_list:
        fout.write("\t".join(item)+"\n")
    print(line_cnt)
    
fout.close()
