
import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd
from math import *
import datetime
from cut import cut_image
import shutil

# main functionality for labeling
# create 4 directories in the same folder
# 1. resource : images waiting to be cut labeled
# 2. results  : result images pieces
# 3. dones    : images already cut and labeled
# 4. wrong    : images already cut (and labeled) but produce wrong number of pieces.

# create 3 files for information
# 1. label.csv  : labeling results (0-3)
# 2. number.txt : current pieces number
# 3. wrongs.txt : pieces that has been mis-labeled.


path = './resource/'
resPath = './resource/results/'
donePath = './resource/dones/'
wrongPath = './resource/wrongs/'

with open('./number.txt', 'r') as f:
    count = f.read()
count = int(count)


for file in os.listdir(path):
    print(file)
    if not file.lower().endswith(".jpg"):
        continue
    originImg = cv2.imread(path + file) 
    # plt.imshow(originImg)
    cuts,boxlist,res = cut_image(originImg)
    lastname = ""
    for imgOut in cuts:
        now = datetime.datetime.now()
        filename = str(now.strftime("%d-%H-%M-%S"))
        num_of_pages = str(count)
        filename = resPath+filename + '_'+ num_of_pages +'.jpg'
        cv2.imwrite(filename, imgOut)
        count = count+1
        cv2.imshow("imgOut", imgOut)  # 裁减得到的旋转矩形框
        keycode=cv2.waitKey(0)
        cv2.destroyAllWindows()
        label = keycode - ord('0') - 1
        if label > 4 :
            with open('./wrongs.txt', 'a+') as wrongs:
                wrongs.write(lastname + "\n")
            label = label - 4
        lastname = filename
        dataframe = pd.DataFrame({'filename':[filename],'label':[label]})
        dataframe.to_csv('label.csv', mode='a', index=False, header=False)   
    if not len(cuts) == 10:
        shutil.move(path+file,wrongPath+file)
    else :
        shutil.move(path+file,donePath+file)
       
with open('./number.txt', 'w') as f:
    f.write(str(count))