from Cutter.cut import cut_image
from Cutter.color import detect_color
from Classifier.CapDetect import CapDectect


# main fuctionality for detecting caps
# input the image 
# return the boxlist(array of  4-points), colorList(array of RGB(array)), imagelist(array of cut images)


def detect(image):
    classifier = CapDectect()
    imagelist,boxlist,markedImage = cut_image(image)
    colorList = detect_color(imagelist)
    
    classlist = []
    for image in imagelist:
        classlist.append(classifier.predict(image))

    return boxlist,colorList,imagelist,classlist


def test():
    import os  
    import cv2
    import datetime
    path = './resource/dones/'

    for file in os.listdir(path):
        print(file)
        if not file.lower().endswith(".jpg"):
            continue
        originImg = cv2.imread(path + file) 
        boxlist,colorlist,imagelist,classlist = detect(originImg)
        print("boxlist",boxlist)
        print("colorlist",colorlist)
        print("classlist",classlist)
        input()

if __name__ == "__main__":
    test()

        