
import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd
from math import *
import datetime
from cut import cut_image
import shutil

# main functionality for labeling
path = './resource/'
resPath = './results/'
donePath = './dones/'
with open('./number.txt', 'r') as f:
    count = f.read()
count = int(count)


for file in os.listdir(path):
    print(file)
    if not ".jpg" in file:
        continue
    originImg = cv2.imread(path + file) 
    # plt.imshow(originImg)
    cuts,res = cut_image(originImg)
    lastname = ""
    for imgOut in cuts:
        now = datetime.datetime.now()
        filename = str(now.strftime("%d-%H-%M-%S"))
        num_of_pages = str(count)
        filename = resPath+filename + '_'+ num_of_pages +'.jpg'
        
        cv2.imwrite(filename, imgOut)
        count = count+1
        # plt.imshow(imgOut)
        # plt.figure()
        cv2.imshow("imgOut", imgOut)  # 裁减得到的旋转矩形框
        keycode=cv2.waitKey(0)
        cv2.destroyAllWindows()
        label = keycode - ord('0')
        if label > 4 :
            with open('./wrongs.txt', 'a+') as wrongs:
                wrongs.write(lastname + "\n")
            label = label - 4
        lastname = filename
        dataframe = pd.DataFrame({'filename':[filename],'label':[label]})
        dataframe.to_csv('label.csv', mode='a', index=False, header=False)   
    shutil.move(path+file,donePath+file)
       
with open('./number.txt', 'w') as f:
    f.write(str(count))