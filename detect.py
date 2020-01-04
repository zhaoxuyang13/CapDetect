from Cutter.cut import cut_image
from Cutter.color import detect_color
from Classifier.CapDetect import CapDectect
import cv2

# main fuctionality for detecting caps
# input the image 
# return the boxlist(array of  4-points), colorList(array of RGB(array)), imagelist(array of cut images)


def detect(image):
    classifier = CapDectect()
    imagelist,boxlist,markedImage = cut_image(image)
    colorList = detect_color(imagelist)
    print(colorList)
    classlist = []
    for image,color in zip(imagelist,colorList):
        classlist.append(classifier.predict(image))
        name = classifier.predict(image)
        # cv2.imshow(str(name) + ":" + color[1],image) 
        # # print(color[1])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
 

    return boxlist,colorList,imagelist,classlist,markedImage


def test():
    import os  
    import cv2
    import datetime
    path = './resource/wrongs/'

    for file in os.listdir(path):
        print(file)
        if not file.lower().endswith(".jpg"):
            continue
        originImg = cv2.imread(path + file) 
        boxlist,colorlist,imagelist,classlist,res = detect(originImg)
        print("boxlist",boxlist)
        print("colorlist",colorlist)
        print("classlist",classlist)

if __name__ == "__main__":
    test()

        