# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:46:18 2021

@author: Леонид
"""
import pyautogui
import cv2
import numpy as np

def shot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("LastMadeShot.png", image)
    return image

def maskSlide(img):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower=np.array([0,0,107])
    upper=np.array([179,8,255])
    mask=cv2.inRange(imgHSV,lower,upper)
    imResult=cv2.bitwise_and(img,img,mask=mask)
    return imResult


def getContours(img,imgC):
    imgContor=imgC.copy()
    countours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    z=0
    for cnt in countours:
        area= cv2.contourArea(cnt)
        if area>50000:
            peri =cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
            imgContor=imgContor[y:y+h,x:x+w]
            z=area
           
    return [imgContor,z]

def Cut():
    orig=shot()
    img=maskSlide(orig)
    d=0
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny =cv2.Canny(imgBlur,50,50)
    imgContor, d= getContours(imgCanny,orig)
    print(d)
    
    cv2.imshow("d"+str(d), imgContor)
  
    cv2.waitKey(0)
        
Cut()
