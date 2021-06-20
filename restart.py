# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 18:31:36 2020

@author: pang
"""

import directkeys
from PIL import ImageGrab
import time
import numpy as np
from grabscreen import grab_screen
import cv2

def get_self_blood():
    blood_window_gray = np.array(ImageGrab.grab(bbox=(directkeys.blood_window)))
    blood = directkeys.self_blood_count(blood_window_gray)
    print("当前血量:")
    print(blood)
    return blood

def reborn():
    print("死")
    time.sleep(3)
    print("复活")
    directkeys.attack()
    time.sleep(2)
    directkeys.lock_vision()
    print("开始新一轮")


def restart():
    print("等死")
    while(True):
        if (get_self_blood() < 10):
            break
    reborn()

if __name__ == "__main__":  
    restart()