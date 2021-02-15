# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:46:18 2021

@author: Леонид
"""
import threading
from tkinter import *
import time
import pyautogui
import cv2
import numpy as np


def Start():
    global On
    On=False
    
Start()
    
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
    for cnt in countours:
        area= cv2.contourArea(cnt)
        if area>50000:
            peri =cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
            imgContor=imgContor[y:y+h,x:x+w]
    return imgContor

def whiteCount(img):
    d=0
    x=y=0
    for row in img:
        x=x+1
        y=0
        for line in row:
            y=y+1

    print("x=",x," ,y=",y)
    return d
            
def CountDifs(img):
    dif =0
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny =cv2.Canny(imgBlur,50,50)
    countours,hierarchy=cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in countours:
        dif=dif+cv2.arcLength(cnt,True)
    return dif

def Cut():
    orig=shot()
    img=maskSlide(orig)
    d=0
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny =cv2.Canny(imgBlur,50,50)
    imgContor= getContours(imgCanny,orig)
    d=CountDifs(imgContor)
    return imgContor,d

def scan():
    sec=1
    global On
    prev,f=Cut()
    while sec<200 and On:
        sec=sec+1
        img,d = Cut()
        if abs(d-f)>2000:
    
            cv2.imwrite("R/Shot"+str(sec)+".png", prev)
        print(d)
        time.sleep(1)
        prev,f = img,d 
        
def turn():
    global On
    if On:
        On=False
        print("Stopped")
    else:
        On=True
        t = threading.Thread(target=scan)
        t.start()
        print("Started")

root = Tk()
Start()
root['bg']='#aafafa'
root.title("ScreenShooter")
root.wm_attributes('-alpha',0.7)
root.geometry('300x300')
root.resizable(width=False, height=False)
frame=Frame(root,bg='black')
frame.place(relx=0.15, rely=0.15, relwidth=0.7,relheight=0.7)
btn=Button(frame,text="Start", bg='yellow', command= turn)
btn.pack()
print(On)

root.mainloop()
    

    