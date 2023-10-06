import urllib
from urllib import request
from bs4 import BeautifulSoup
import time
import datetime
import random
import sys
import os
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

#HOST = "http://bmfw.www.gov.cn/yqfxdjcx/risk.html"
HEADERS={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}


#driver=webdriver.Firefox()
#driver.set_page_load_timeout(15)

def get_risk_area_cnt():
    HOST = "https://bj.bendibao.com/news/gelizhengce/fengxianmingdan.php"
    #driver.get(HOST)
    req = urllib.request.Request(url=HOST, headers=HEADERS)
    page_html = urllib.request.urlopen(req).read()
    high_risk_list = {}
    #bs4Page=BeautifulSoup(driver.page_source,"html.parser")
    bs4Page=BeautifulSoup(page_html,"html.parser")
    high_risk_div = bs4Page.find("div",{"class":"height"})
    city_div=high_risk_div.findAll("div",{"class":"detail-message"})
    for item in city_div:
        province_and_city_name = item.find("span",{"class":"city"}).text.replace("\n"," ").strip(" ").split()
        province_name = province_and_city_name[0]
        if province_name[-1] in ("省","市"):
            province_name = province_name[:-1]
        province_name = province_name.replace("壮族自治区","").replace("维吾尔自治区","").replace("回族自治区","").replace("自治区","")
        if len(province_and_city_name)==1:
            city_name = province_and_city_name[0]
        else:
            city_name = province_and_city_name[1]
        if city_name[-1] in ("省","市"):
            city_name = city_name[:-1]
        area_cnt = int(item.find("span",{"class":"much"}).text.replace("个",""))

        if province_name not in high_risk_list:
            high_risk_list[province_name] = {}
        high_risk_list[province_name][city_name] = area_cnt
        #high_risk_list.append((province_name, city_name, area_cnt))

    #for item in high_risk_list:
    #    print(province_name + "\t" + city_name + "\t" + str(item[2]))
    return high_risk_list

def get_patient_cnt():
    HOST = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
    #HOST = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    #driver.get(HOST)
    req = urllib.request.Request(url=HOST, headers=HEADERS)
    page_text = urllib.request.urlopen(req).read().decode("utf8")
    patient_cnt_list = {}
    #bs4Page=BeautifulSoup(driver.page_source,"html.parser")
    page_json=json.loads(page_text)
    world_list = page_json["data"]["areaTree"]
    china_list = []
    for item in world_list:
        if item["name"]=="中国":
            china_list = item["children"]
            break
    for item1 in china_list:
        patient_cnt_list[item1["name"]] = {}
        if item1["name"] in ("北京","上海","天津","重庆"):
            patient_cnt_list[item1["name"]][item1["name"]] = item1["today"]["confirm"]
            continue
        #patient_cnt_list.append((item1["name"], item1["name"], item1["today"]["confirm"]))
        #if item1["today"]["confirm"]>0:
        #        print("\t".join([item1["name"], item1["name"], str(item1["today"]["confirm"])]))
        for item2 in item1["children"]:
            if ("境外" in item2["name"]) or ("未明确" in item2["name"]) or ("待确认" in item2["name"]) or ("外地" in item2["name"]):
                continue
            if item2["today"]["confirm"]>0:
                patient_cnt_list[item1["name"]][item2["name"]] = item2["today"]["confirm"]
            #patient_cnt_list.append((item1["name"], item2["name"], item2["today"]["confirm"]))
            #if item2["today"]["confirm"]>0:
            #    print("\t".join([item1["name"], item2["name"], str(item2["today"]["confirm"])]))
    return patient_cnt_list



a=get_risk_area_cnt()
b=get_patient_cnt()
today = datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d")
out_text=json.dumps({"risk_area":a,"infecion_cnt":b})
fout=open("pandemic_info_%s.json"%today,"w",encoding="utf8")
fout.write(out_text)
fout.close()


