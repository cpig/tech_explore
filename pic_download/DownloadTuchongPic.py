import urllib.request
import codecs
import time
import random
import sys
import os

UserId=sys.argv[1]
UpperBound=100000000
LowerBound=0
if int(sys.argv[2])<UpperBound:
    UpperBound=int(sys.argv[2])
if int(sys.argv[3])>LowerBound:
    LowerBound=int(sys.argv[3])
    
if not os.path.exists("TC_"+UserId):
    os.mkdir("TC_"+UserId)
for i in range(LowerBound,UpperBound):
    try:
        urllib.request.urlretrieve("http://photo.tuchong.com/"+UserId+"/f/"+str(i)+".jpg","TC_"+UserId+"\\"+str(i)+".jpg")
    except:
        pass
    if i%100==0:
        print(i)
        
