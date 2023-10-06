import time
import datetime
import random
import sys
import os
import json

def get_date_list():
    result = []
    for i in range(7):
        result.append(datetime.datetime.now()-datetime.timedelta(i))
    return result

def load_crawling_result(date_list):
    result = []
    for date_item in date_list:
        file_name = "pandemic_info_%s.json"%(datetime.datetime.strftime(date_item, "%Y%m%d"))
        print("loading %s ..."%file_name)
        try:
            result.append(json.loads(open(file_name,"r").read()))
        except:
            result.append({})
    return result

def get_template():
    print("loading pandemic.htm ...")
    return open("pandemic.htm","r",encoding="utf8").read()

def get_city_list():
    print("loading city_list.txt ...")
    result = []
    for line in open("city_list.txt","r",encoding="utf8"):
        result.append(line.strip().split())
    return result

def filling_template(html_template, date_list, city_list, data):
    html_wildcard = html_template.replace(r"%%%", "%s")
    filling_string_list = []
    for date_item in date_list:
        filling_string_list.append(datetime.datetime.strftime(date_item, "%m-%d"))
    for date_item in date_list:
        filling_string_list.append(datetime.datetime.strftime(date_item, "%m-%d"))
    for city_item in city_list:
        for i in range(7):
            try:
                filling_string_list.append(str(data[i]["risk_area"][city_item[0]][city_item[1]]))
            except:
                filling_string_list.append("--")
        for i in range(7):
            try:
                filling_string_list.append(str(data[i]["infecion_cnt"][city_item[0]][city_item[1]]))
            except:
                filling_string_list.append("--")
    #print("len=%i"%(len(filling_string_list)))
    return html_wildcard%tuple(filling_string_list)

date_list = get_date_list()
data_set = load_crawling_result(date_list)
html_template = get_template()
city_list = get_city_list()
output_html = filling_template(html_template, date_list, city_list, data_set)

fout = open("output.htm", "w", encoding="utf8")
fout.write(output_html)
fout.close()

