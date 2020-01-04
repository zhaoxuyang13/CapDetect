# -*- coding: utf-8 -*-
import torch
from .model import CapCNN
import numpy as np
import cv2

class CapDectect():
    def __init__(self):
        super(CapDectect,self).__init__()
        self.model = CapCNN()
        self.model.load_state_dict(torch.load('Classifier/para/cap_para.pkl',map_location='cpu'))
        
    def predict(self,img):
        img_hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
        _,s,_ = cv2.split(img_hsv)
        s = s[np.newaxis,np.newaxis,:,:]
        Xtest = s/255.0
        Xtest = torch.from_numpy(Xtest)
        Xtest = Xtest.type(torch.FloatTensor)
        with torch.no_grad():
            outputs = self.model(Xtest)
            _, predicted = torch.max(outputs.data, 1)
            predicted = np.array(predicted)
        return predicted[0]
    
def main():
    model = CapDectect()
    img = cv2.imread('sample.jpg')
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    predicted_label = model.predict(img)
    print(predicted_label)

if __name__ == '__main__':
    main()