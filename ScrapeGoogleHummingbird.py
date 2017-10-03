#from urllib.request import urlopen
from bs4 import BeautifulSoup
import codecs
import time
import random
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver=webdriver.Firefox()
#driver.get("https://www.google.com/search?safe=strict&hl=en-US&q=how many countries in the world")
driver.get("https://www.google.com/ncr")
time.sleep(random.randint(3000,8000)/1000)
#driver.get("https://www.google.com/#q=now the test begin")
#lastQueryLength=len("now the test begin")
#time.sleep(random.randint(3000,8000)/1000)
lastQueryLength=5

fin=codecs.open("HBquery.tsv","r","utf-8")
success_out=codecs.open("passage.tsv","a","utf-8")
fail_out=codecs.open("failedQuery.tsv","a","utf-8")
queryCount=0
try:
    queryCountInput=open("TempQueryCount","r")
    queryCount=int(queryCountInput.read().strip())
    queryCountInput.close()
except:
    queryCount=0
for i in range(queryCount):
    fin.readline()


for line in fin:
    '''
    if queryCount%20==0:
        driver.quit()
        queryCountOutput=open("TempQueryCount","w")
        queryCountOutput.write(str(queryCount))
        queryCountOutput.close()
        time.sleep(random.randint(60,150))
        driver=webdriver.Firefox()
        driver.get("https://www.google.com/ncr")
        time.sleep(random.randint(3000,8000)/1000)
        driver.get("https://www.google.com/#q=what does continue mean")
        lastQueryLength=len("what does continue mean")
        time.sleep(random.randint(3000,8000)/1000)
    '''
    try:
        query=line.strip()
        inputElement=driver.find_element_by_id("lst-ib")
        for i in range(lastQueryLength+5):
            time.sleep(random.randint(20,50)/1000)
            inputElement.send_keys("\b")
        inputElement.clear()
        lastQueryLength=len(query)
        for char in query:
            time.sleep(random.randint(30,100)/1000)
            inputElement.send_keys(char)
        time.sleep(random.randint(20,100)/1000)
        inputElement.send_keys("\n")
    #button=driver.find_element_by_id("sblsbb").find_element_by_class_name("lsb")
    #button.click()
        time.sleep(5)
    except:
        fail_out.write(query+"\r\n")
        queryCountOutput=open("TempQueryCount","w")
        queryCountOutput.write(str(queryCount))
        queryCountOutput.close()
        success_out.close()
        fail_out.close()
        driver.quit()
        time.sleep(random.randint(60,180))
        driver=webdriver.Firefox()
        driver.get("https://www.google.com/ncr")
        time.sleep(random.randint(3000,8000)/1000)
        #driver.get("https://www.google.com/#q=what does continue mean")
        #lastQueryLength=len("what does continue mean")
        #time.sleep(random.randint(3000,8000)/1000)
        continue
        
    try:
        bs4Page=BeautifulSoup(driver.page_source,"html.parser")
        answer=bs4Page.find(class_="_OKe")
        if not answer.find(class_="_Tgc")==None:
            passage=answer.find(class_="_Tgc").decode_contents().replace('\n','<br/>')#.get_text()
        elif not answer.find(class_="mod")==None:
            tempAnswer=answer.find(class_="mod")
            if "mod" in tempAnswer.findNextSibling().attrs["class"]:
                passage=tempAnswer.findNextSibling().decode_contents().replace('\n','<br/>')
            else:
                passage=tempAnswer.decode_contents().replace('\n','<br/>')
        elif not answer.find(name="table")==None:
            passage=answer.find(name="table").decode().replace('\n','<br>')
        elif not answer.find(name="ol")==None:
            passage=answer.find(name="ol").decode().replace('\n','<br>')
        titleAndUrl=answer.find(class_="g").h3.a
        url=titleAndUrl.attrs["href"]
        title=titleAndUrl.get_text()
        success_out.write(query+"\t"+passage+"\t"+url+"\t"+title+"\r\n")
    except:
        fail_out.write(query+"\r\n")
        
    queryCount+=1
    
    try:
        time.sleep(random.randint(3000,30000)/1000)
    except:
        queryCountOutput=open("TempQueryCount","w")
        queryCountOutput.write(str(queryCount))
        queryCountOutput.close()
        success_out.close()
        fail_out.close()
        driver.quit()
        time.sleep(random.randint(60,180))
        driver=webdriver.Firefox()
        driver.get("https://www.google.com/ncr")
        time.sleep(random.randint(3000,8000)/1000)
        #driver.get("https://www.google.com/#q=what does continue mean")
        #lastQueryLength=len("what does continue mean")
        #time.sleep(random.randint(3000,8000)/1000)
        
fin.close()
success_out.close()
fail_out.close()
driver.quit()
queryCountOutput=open("TempQueryCount","w")
queryCountOutput.write(str(queryCount))
queryCountOutput.close()
        
        
    
