from cut import cut_image
from color import detect_color



# main fuctionality for detecting caps
# input the image 
# return the location(as 4 points), 


def detect(image):
    imagelist,boxlist,markedImage = cut_image(image)
    colorList = detect_color(imagelist)
    return boxlist,colorList,imagelist


def test():
    import os  
    import cv2
    import datetime
    path = './dones/'

    for file in os.listdir(path):
        print(file)
        if not file.lower().endswith(".jpg"):
            continue
        originImg = cv2.imread(path + file) 
        boxlist,colorlist,imagelist = detect(originImg)
        print("boxlist",boxlist)
        print("colorlist",colorlist)
        
        input()

test()
        