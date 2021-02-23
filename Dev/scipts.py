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
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

global chat_id
global token
global path


def Start():
    global On
    global bot
    global chat_id
    global token
    On = False
    #bot = telegram.Bot(token="1669054885:AAFrbVf_dDioCB0EWGXJKW-SzeTM1RrAoEo")
    #chat_id = "@storageH"
    #bot.send_photo(chat_id=chat_id, photo=open('LastMadeShot.png', 'rb'))


def shot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("LastMadeShot.png", image)
    return image


def maskSlide(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 107])
    upper = np.array([179, 8, 255])
    mask = cv2.inRange(imgHSV, lower, upper)
    imResult = cv2.bitwise_and(img, img, mask=mask)
    return imResult


def getContours(img, imgC):
    imgContor = imgC.copy()
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area > 50000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            imgContor = imgContor[y:y + h, x:x + w]
    return imgContor


def whiteCount(img):
    d = 0
    x = y = 0
    for row in img:
        x = x + 1
        y = 0
        for line in row:
            y = y + 1

    print("x=", x, " ,y=", y)
    return d


def CountDifs(img):
    dif = 0
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    countours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in countours:
        dif = dif + cv2.arcLength(cnt, True)
    return dif


def Cut():
    orig = shot()
    img = maskSlide(orig)
    d = 0
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    imgContor = getContours(imgCanny, orig)
    d = CountDifs(imgContor)
    return imgContor, d


def scan():
    sec = 1
    print("scanning")
    global On
    global path
    prev, f = Cut()
    while On:
        sec = sec + 1
        img, d = Cut()
        if abs(d - f) > 2000:
            print("It was done.")
            picpath = path + "\Shot" + str(sec) + ".png"
            cv2.imwrite(picpath, prev)
            bot.send_photo(chat_id=chat_id, photo=open(picpath, 'rb'))
        else:
            print("d-f=", (d - f))
        print(edt.get())

        time.sleep(1)
        prev, f = img, d


def turn():
    global On
    if On:
        On = False
        print("Stopped")

    else:
        parse()
        On = True
        t = threading.Thread(target=scan)
        t.start()
        print("Started")


def parse():
    global path
    global token
    global chat_id
    global bot
    path = edt.get()
    tokenfile = open("token.txt", 'r')
    token = tokenfile.read()
    tokenfile.close()

    chatfile = open('id.txt', 'r')
    chat_id = chatfile.read()
    chatfile.close()
    bot = telegram.Bot(token=token)
    print(path," ",token," ",chat_id)


root = Tk()
Start()
root['bg'] = '#aafafa'
root.title("ScreenShooter")
root.wm_attributes('-alpha', 0.7)
root.geometry('300x300')
root.resizable(width=False, height=False)
frame = Frame(root, bg='black')
frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
btn = Button(frame, text="Start/Stop", bg='yellow', command=turn)
btn.pack()
edt = Entry(frame, width=20, bg='yellow')
edt.pack()
print(On)

root.mainloop()


