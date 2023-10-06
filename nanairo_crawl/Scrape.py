import urllib
from bs4 import BeautifulSoup
import codecs
import time
import random
import sys
import os
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

URL_ROOT = "https://nanairo.co/ja/"
URL_ROOT_VIDEO = URL_ROOT + "videos/"
URL_ROOT_CAST = URL_ROOT + "casts/"
driver=webdriver.Firefox()
driver.set_page_load_timeout(10)
VIDEO_UPPER_BOUND = 4640
CAST_UPPER_BOUND = 1475
date_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
#fout = open("video_info_20220313.txt","w",encoding="utf8")


def parse_cast_page(cast_id):
    result = {"id":str(cast_id), "name_en":"", "name":"", "videos":[], "photos":[], "popularity":"", "desc":"",
              "height":"", "size":"", "gender":"", "start_date":"", "comment":""}
    profile_url = URL_ROOT_CAST + str(cast_id) + "/profile"
    logging.info("Opening " + profile_url)
    try:
        driver.get(profile_url)
        bs4_page = BeautifulSoup(driver.page_source,"html.parser")
        result["popularity"] = bs4_page.find("span",{"class":"favorite-count"}).text.strip()
        result["desc"] = bs4_page.find("h2", {"class":"caption"}).text.strip()
        result["comment"] = bs4_page.find("div",{"class":"nn-column-layout"}).find("div",{"class":"nn-card-inner"}).text.strip()
        profile_table = bs4_page.find("table",{"class":"nn-tbl-datasheet"}).findAll("tr")
        result["name_en"] = profile_table[0].find("strong").text.strip()
        result["name"] = profile_table[0].find("td").text.replace(result["name_en"],"").strip()
        logging.info("name: " + result["name"])
        result["height"] = profile_table[1].find("td").text.strip()
        result["gender"] = profile_table[2].find("td").text.strip()
        result["size"] = profile_table[3].find("td").text.strip()
        result["start_date"] = profile_table[4].find("td").text.strip()
    except Exception:
        logging.error(repr(Exception))
    return result

def crawl_cast_info(start, end):
    fout = open("cast_info_%s.tsv"%date_str, "a", encoding="utf8")
    for cast_id in range(start, end+1):
        cast = parse_cast_page(cast_id)
        fout.write("\t".join([cast["id"],cast["name_en"],cast["name"],cast["popularity"],\
                              cast["desc"],cast["height"],cast["size"],cast["gender"],cast["start_date"],cast["comment"]])+"\n")
    fout.close()

def parse_video_page(video_id):
    result = {"id":str(video_id), "title":"", "caption":"", "casts":[], "popularity":"", "desc":"",
              "date":"", "length":"", "labels":[],  "comment":""}
    profile_url = URL_ROOT_CAST + str(cast_id) + "/profile"
    logging.info("Opening " + profile_url)
    video_url = URL_ROOT_VIDEO + str(video_id)
    

def load_page_count_seconds(driver, url, seconds):
    #driver.set_page_load_timeout(seconds)
    try:
        driver.get(url)
    except:
        logging.error("Page loading timeout")
        #driver.execute_script("window.stop()")

'''
for video_id in range(upper_bound, 0, -1):
    fail_cnt = 0
    while fail_cnt<10:
        try:
            time.sleep(1)
            video_page = video_root + str(video_id)
            logging.info("Opening " + video_page)
            #driver.get(video_page)
            load_page_count_seconds(driver, video_page, 10)

            bs4Page = BeautifulSoup(driver.page_source,"html.parser")
            title_h1 = bs4Page.find("h1",{"class":"subject"}).text
            title_h2 = bs4Page.find("h2",{"class":"caption"}).text
            fav_cnt=bs4Page.find("span",{"class":"favorite-count"}).text
            if title_h1+"#"+title_h2 == fn:
                logging.error("Loading new page failed")
                fail_cnt += 1
                continue

            actress = []
            labels = []
            info_pan = bs4Page.find("div",{"class":"nn-column-layout"})
            links = info_pan.find_all("a")
            for link in links:
                if link["href"].startswith("/ja/casts/"):
                    actress.append(link["href"])
                elif link["href"].startswith("/ja/labels/"):
                    labels.append(link["href"])
            date = info_pan.find_all("td")[-1].text
            length = info_pan.find_all("td")[-2].text
            desc = info_pan.find_all("div",{"class":"nn-card-inner"})[-1].text.strip()
            to_write = "\t".join([str(video_id),fav_cnt,title_h1,title_h2,actress[0],labels[0],date, desc, length])
            fout.write(to_write+"\n")
            logging.info(to_write)
            fail_cnt = 10
            last_key = title_h1+"#"+title_h2
        except Exception as e:
            print(str(e))
            fail_cnt += 1
fout.close()'''
crawl_cast_info(1,CAST_UPPER_BOUND)
driver.close()
