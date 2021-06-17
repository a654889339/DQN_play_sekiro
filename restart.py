# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 18:31:36 2020

@author: pang
"""

import directkeys
import time
import numpy as np
from grabscreen import grab_screen
import cv2

def get_self_blood():
    blood_window_gray = cv2.cvtColor(grab_screen(directkeys.blood_window), cv2.COLOR_BGR2GRAY)
    blood = directkeys.self_blood_count(blood_window_gray)
    print("当前血量:")
    print(blood)
    return blood

def reborn():
    print("死")
    time.sleep(2)
    print("复活")
    directkeys.attack()
    time.sleep(1)
    print("作弊")
    directkeys.Cheat()
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