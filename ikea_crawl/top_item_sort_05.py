import sys
import os
import base64
import datetime

today_dt = datetime.datetime.now()
today_str = datetime.datetime.strftime(today_dt, "%Y%m%d")
today_1p_str = datetime.datetime.strftime(today_dt-datetime.timedelta(1), "%Y%m%d")
today_7p_str = datetime.datetime.strftime(today_dt-datetime.timedelta(7), "%Y%m%d")

def get_top_n_item(n):
    fin = open("ikea_top_item_sales.tsv", "r", encoding="utf8")
    item_dict = {}
    total_sales = 0
    for line in fin:
        title, subtitle, link, pic, quantity, price = line.strip().split('\t')
        quantity = int(quantity)
        pic = pic.split('/')[-1]
        price_float = float(price)
        skuid = link.strip('/').split('/')[-1]
        if not skuid in item_dict:
            item_dict[skuid] = (title, subtitle, pic, quantity, price, price_float*quantity)
            total_sales += quantity*price_float
        else:
            if quantity!=item_dict[skuid][3]:
                print(skuid)
        item_sort = sorted(item_dict.items(), key=lambda x:x[1][3], reverse=True)
        #item_sort = sorted(item_dict.items(), key=lambda x:x[1][5], reverse=True)
    return item_sort[:n], total_sales

def output_top_items_tsv(top_items):
    fout= open("ikea_top_item_sorted_%s.tsv"%today_str, "w", encoding="utf8")
    #item_sort = get_top_n_item(300)
    for item in top_items:
        fout.write("\t".join([item[1][0], item[1][1], str(item[1][3]), item[1][4], item[0], item[1][2]]) + "\n")
    fout.close()
    
def output_top_items_html_base64(top_items, last_rank, total_sales):
    html_doc = ""
    html_doc += open("rank_header_template.txt", "r", encoding="utf8").read()
    html_doc += """
<li style="list-style:none;background:#fff;position:relative;float:left;margin:0 5px 10px;width:1300px;height:180px">
<div style="display:block;margin:10px 50px auto">
<p style="font-size:30px;line-height:40px">一周销售额测算 %s-%s</p>
<p style="font-size:30px;line-height:40px">￥%.2f亿（含税）</p>
</div>
</li>
"""%(today_7p_str, today_1p_str, total_sales/100000000)
    item_template = open("rank_item_template.txt", "r", encoding="utf8").read()
    item_cnt=0
    for item in top_items:
        item_cnt+=1
        img_base64 = base64.b64encode(open("pic/"+item[1][2], "rb").read())
        if item[0] in last_rank:
            rank_diff = last_rank[item[0]]-item_cnt
            if abs(rank_diff)/item_cnt<0.1:
                rank_diff_str = ""
            elif rank_diff>0:
                rank_diff_str = "(上升%i)"%rank_diff
            elif rank_diff<0:
                rank_diff_str = "(下降%i)"%(-rank_diff)
            #elif rank_diff==0:
            #    rank_diff_str = "持平"
        else:
            rank_diff_str = "(新上榜)"
        html_doc += item_template%(item[0], "data:image/jpg;base64,"+img_base64.decode("utf8"), "%i  "%item_cnt+rank_diff_str, item[1][1], item[1][3], item[1][4])
    html_doc += '</ul></div></body></html>'
    fout = open("ikea_top_items_base64_qty_%s.html"%today_str, "w", encoding="utf8")
    fout.write(html_doc)
    fout.close()

def output_top_items_html_base64_sales():
    html_doc = ""
    html_doc += open("rank_header_template.txt", "r", encoding="utf8").read()
    item_sort = get_top_n_item(500)
    item_template = open("rank_item_template_sales.txt", "r", encoding="utf8").read()
    item_cnt=0
    for item in item_sort:
        item_cnt+=1
        img_base64 = base64.b64encode(open("pic/"+item[1][2], "rb").read())
        html_doc += item_template%(item[0], "data:image/jpg;base64,"+img_base64.decode("utf8"), "第%i名  "%item_cnt, item[1][1]+" "+item[1][0], str(item[1][5]))
    html_doc += '</ul></div></body></html>'
    fout = open("ikea_top_items_base64_sales.html", "w", encoding="utf8")
    fout.write(html_doc)
    fout.close()

def get_html():
    html_doc = ""
    html_doc += open("rank_header_template.txt", "r", encoding="utf8").read()
    item_sort = get_top_n_item(50)
    item_template = open("rank_item_template.txt", "r", encoding="utf8").read()
    pic_list = []
    for item in item_sort:
        html_doc += item_template%(item[0], item[1][2], item[1][1], item[1][3], item[1][4])
        pic_list.append(item[1][2])
    html_doc += '</ul></div></body></html>'
    return html_doc, pic_list

def get_html_base64():
    html_doc = ""
    html_doc += open("rank_header_template.txt", "r", encoding="utf8").read()
    item_sort = get_top_n_item(400)
    item_template = open("rank_item_template.txt", "r", encoding="utf8").read()
    item_cnt=0
    for item in item_sort:
        item_cnt+=1
        img_base64 = base64.b64encode(open("pic/"+item[1][2], "rb").read())
        html_doc += item_template%(item[0], "data:image/jpg;base64,"+img_base64.decode("utf8"), "第%i名  "%item_cnt+item[1][1], item[1][3], item[1][4])
    html_doc += '</ul></div></body></html>'
    return html_doc

def get_last_rank():
    historical_rank_dir = "rank_backup/"
    filename = sorted(os.listdir(historical_rank_dir))[-1]
    item2rank = {}
    rank = 0
    for line in open(historical_rank_dir+filename, "r", encoding="utf8"):
        rank += 1
        name, desc, qty, price, item_id, item_pic = line.strip('\n').split('\t')
        item2rank[item_id] = rank
    return item2rank


top_items, total_sales = get_top_n_item(400)
output_top_items_tsv(top_items)
last_rank = get_last_rank()
output_top_items_html_base64(top_items, last_rank, total_sales)
#output_top_items_html_base64()
