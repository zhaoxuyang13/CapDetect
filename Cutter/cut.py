#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
# import matplotlib.pyplot as plt
from math import *

## reference 
# 物体识别 https://blog.csdn.net/liqiancao/article/details/55670749
# 旋转矩形框裁剪 https://blog.csdn.net/yjl9122/article/details/71217872


def rotateImage(img, degree, pt1, pt2, pt3, pt4): 
  print(pt1,pt2,pt3,pt4)
  height, width = img.shape[:2]
  heightNew = int(width * fabs(sin(radians(degree))) +
                  height * fabs(cos(radians(degree))))
  widthNew = int(height * fabs(sin(radians(degree))) +
                  width * fabs(cos(radians(degree))))
  matRotation = cv2.getRotationMatrix2D((width//2, height//2), degree, 1)
  # print(matRotation)
  matRotation[0, 2] += (widthNew - width) / 2
  matRotation[1, 2] += (heightNew - height) / 2
  print(matRotation)
  imgRotation = cv2.warpAffine(
      img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
  pt1 = list(pt1)
  pt3 = list(pt3)
  [[pt1[0]], [pt1[1]]] = np.dot(
      matRotation, np.array([[pt1[0]], [pt1[1]], [1]]))
  [[pt3[0]], [pt3[1]]] = np.dot(
      matRotation, np.array([[pt3[0]], [pt3[1]], [1]]))
  # print(pt1,pt3,pt2,pt4)
  xmin = np.max([np.min([pt1[1],pt3[1]]),0])
  xmax = np.min([np.max([pt1[1],pt3[1]]),imgRotation.shape[0]])
  ymin = np.max([np.min([pt1[0],pt3[0]]),0])
  ymax = np.min([np.max([pt1[0],pt3[0]]),imgRotation.shape[1]])
  # print(xmin,xmax,ymin,ymax)
  imgOut = imgRotation[int(xmin):int(xmax), int(ymin):int(ymax)]
  return imgOut


def cut_image(origin):
# origin = cv2.imread("./resource/IMG_20191218_155712_1.jpg")
    hsv = cv2.cvtColor(origin,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    # plt.imshow(s)
    # gray = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)
    # plt.imshow(gray)
    # 1. thresholding, remove points with low s value.  often margin
    (_, gray) = cv2.threshold(s, 35, 255, cv2.THRESH_TOZERO)
    
    # 2. use solbel to compute gradient of X/Y direction 
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    gradient = cv2.add(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blurred = cv2.medianBlur(gradient, 9)

    (_, thresh) = cv2.threshold(gradient, 35, 255, cv2.THRESH_BINARY)
    # plt.imshow(thresh)
    
    # plt.imshow(cl)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    cl = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    closed = cv2.morphologyEx(cl, cv2.MORPH_CLOSE, kernel)
    # plt.imshow(closed)

    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    # plt.imshow(closed)

    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ct = 0
    ls = []
    res = np.copy(origin)
    cuts = []
    boxlist = []
    for c in cnts:
        if len(c) <= 200:
            print(len(c))
            continue
        # compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))
        imgOut = rotateImage(origin, -degrees(atan2(box[1][0]-box[0][0],box[1][1]-box[0][1])), box[0], box[1], box[2], box[3])
        h,w,d = imgOut.shape
        height,width,d = origin.shape
        if h > height//2 or w > width//2 or h <=50 or w <= 50:
          continue

        ct = ct + 1
        ls.append(len(c))

        imgOut = cv2.resize(imgOut, (100, 100))
        cuts.append(np.copy(imgOut))
        boxlist.append(box)
        for i in box:
            res = cv2.circle(res,(i[0],i[1]),15,(0, 0, 255),8)
        # draw a bounding box arounded the detected barcode and display the image
        res = cv2.drawContours(res, [box], -1, (0, 255, 0), 10)
    # plt.imshow(res)
    
    if not ct == 10:
      print(ct) 
      print(ls)
    
    return (cuts,boxlist,res)
