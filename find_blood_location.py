# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:45:04 2020

@author: pang
"""

import numpy as np
from PIL import ImageGrab
import cv2
import time
import grabscreen
import os

blood_heigh_begin = 70
blood_weight_begin = 53

blood_heigh_len=370
self_blood_len = 242
xieyilang_blood_len = 203
window_size = (220,50,604,394)#384,344  192,172 96,86
blood_window = (blood_weight_begin,blood_heigh_begin,blood_weight_begin+self_blood_len,blood_heigh_begin+blood_heigh_len)
#blood_window = (blood_weight_begin,blood_heigh_begin,blood_weight_begin+self_blood_len,blood_heigh_begin+20)

def self_blood_count(self_gray):
    blood = 0
    #print("self_gray type:")
    #print(type(self_gray))
    #print(len(self_gray))
    #print(len(self_gray[0]))

    for i in range(self_blood_len-1):
        bd_num=self_gray[blood_heigh_len-2][i]
        #print(type(self_bd_num))
        # self blood gray pixel 80~98
        # 血量灰度值80~98
        #print(self_bd_num)
        if bd_num[0] > 120 and bd_num[0] < 130:
            if bd_num[1] > 55 and bd_num[1] < 65:
                if bd_num[2] >  35 and bd_num[2] < 50:
                    blood += 1
    #print("狼血量:")
    #print(blood)
    return blood

def boss_blood_count(boss_gray):
    blood = 0
    #print(type(boss_gray))
    #print(len(boss_gray))
    #print(len(boss_gray[1]))
    #bd_min = [1000,1000,1000]
    #bd_max = [0,0,0]
    for i in range(xieyilang_blood_len):
        bd_num=boss_gray[3][i]
        #print(bd_num)
        #for i in range(3):
        #    bd_min[i] = min(bd_min[i],bd_num[i])
        #    bd_max[i] = max(bd_max[i],bd_num[i])

        if bd_num[0] > 80 and bd_num[0] < 110:
            if bd_num[1] > 25 and bd_num[1] < 50:
                if bd_num[2] >  25 and bd_num[2] < 50:
                    blood += 1

    #print("blood range")
    #for i in range(3):
    #    print("Value:")
    #    print(i)
#        print(bd_min[i])
    #    print(bd_max[i])

    #print("Boss血量:")
    #print(blood)
    return blood

wait_time = 1
L_t = 3

for i in list(range(wait_time))[::-1]:
    print(i+1)
    time.sleep(1)

last_time = time.time()
while(True):

    #printscreen_numpy = np.array(printscreen_pil.getdata(),dtype='uint8')\
    #.reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
    #pil格式耗时太长
    
    screen_gray = np.array(ImageGrab.grab(bbox=(blood_window))) #cv2.cvtColor(grabscreen.grab_screen(blood_window),cv2.COLOR_BGR2GRAY)#灰度图像收集
    # screen_reshape = cv2.resize(screen_gray,(96,86))
    #self_blood = self_blood_count(screen_gray)
    boss_blood = boss_blood_count(screen_gray)


    cv2.imshow('window1',screen_gray)

    printscreen = np.array(ImageGrab.grab(bbox=(window_size)))
    cv2.imshow('window3',printscreen)
    #cv2.imshow('window2',screen_reshape)
    
    #测试时间用
    print('loop took {} seconds'.format(time.time()-last_time))
    last_time = time.time()
    
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    time.sleep(1)
cv2.waitKey()# 视频结束后，按任意键退出
cv2.destroyAllWindows()
