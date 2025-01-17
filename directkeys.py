# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:37:50 2020

@author: pang
"""
#bilibili.com/read/cv9217614
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

M = 0x32
J = 0x24
K = 0x25
LSHIFT = 0x2A
R = 0x13#用R代替识破
V = 0x2F

Q = 0x10
I = 0x17
O = 0x18
P = 0x19
C = 0x2E
F = 0x21

up = 0xC8
down = 0xD0
left = 0xCB
right = 0xCD

number6=0x4D
number7=0x47

esc = 0x01
ctrl=0x1D

blood_heigh_begin = 70
blood_weight_begin = 53

blood_heigh_len=370
self_blood_len = 242
xieyilang_blood_len = 203

window_size = (220,50,604,394)#384,344  192,172 96,86
blood_window = (blood_weight_begin,blood_heigh_begin,blood_weight_begin+self_blood_len,blood_heigh_begin+blood_heigh_len)
def self_blood_count(self_gray):
    blood = 0
    #print("self_gray type:")
    #print(type(self_gray))
    #print(len(self_gray))
    #print(len(self_gray[0]))
    for i in range(len(self_gray[0])):
        bd_num=self_gray[blood_heigh_len-2][i]
        #print("bd_num type:")
        #print(type(bd_num))
        #print(len(bd_num))
        if bd_num[0] > 120 and bd_num[0] < 130:
            if bd_num[1] > 55 and bd_num[1] < 65:
                if bd_num[2] >  35 and bd_num[2] < 50:
                    blood += 1
    return blood

def boss_blood_count(boss_gray):
    blood = 0
    #print("boss_gray type:")
    #print(type(boss_gray))
    #print(len(boss_gray))
    #print(len(boss_gray[0]))
    for i in range(xieyilang_blood_len):
        bd_num=boss_gray[3][i]
        #print("bd_num type:")
        #print(type(bd_num))
        #print(len(bd_num))
        if bd_num[0] > 80 and bd_num[0] < 110:
            if bd_num[1] > 25 and bd_num[1] < 50:
                if bd_num[2] >  25 and bd_num[2] < 50:
                    blood += 1

    return blood

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    
def defense():
    PressKey(M)
    time.sleep(0.05)
    ReleaseKey(M)
    #time.sleep(0.1)
    
def attack():
    PressKey(J)
    time.sleep(0.05)
    ReleaseKey(J)
    #time.sleep(0.1)
    
def go_forward():
    PressKey(W)
    time.sleep(0.4)
    ReleaseKey(W)
    
def go_back():
    PressKey(S)
    time.sleep(0.4)
    ReleaseKey(S)
    
def go_left():
    PressKey(A)
    time.sleep(0.4)
    ReleaseKey(A)
    
def go_right():
    PressKey(D)
    time.sleep(0.4)
    ReleaseKey(D)
    
def jump():
    PressKey(K)
    time.sleep(0.1)
    ReleaseKey(K)
    #time.sleep(0.1)
    
def dodge():#闪避
    PressKey(R)
    time.sleep(0.1)
    ReleaseKey(R)
    #time.sleep(0.1)
    
def lock_vision():
    PressKey(V)
    time.sleep(0.3)
    ReleaseKey(V)
    time.sleep(0.1)

def go_forward_QL(t):
    PressKey(W)
    time.sleep(t)
    ReleaseKey(W)
    
def turn_left(t):
    PressKey(left)
    time.sleep(t)
    ReleaseKey(left)
    
def turn_up(t):
    PressKey(up)
    time.sleep(t)
    ReleaseKey(up)
    
def turn_right(t):
    PressKey(right)
    time.sleep(t)
    ReleaseKey(right)
    
def F_go():
    PressKey(F)
    time.sleep(0.5)
    ReleaseKey(F)
    
def forward_jump(t):
    PressKey(W)
    time.sleep(t)
    PressKey(K)
    ReleaseKey(W)
    ReleaseKey(K)
    
def press_esc():
    PressKey(esc)
    time.sleep(0.3)
    ReleaseKey(esc)
    
def dead():
    PressKey(M)
    time.sleep(0.5)
    ReleaseKey(M)

def Cheat():
    print("屑一郎")

    PressKey(ctrl)
    PressKey(number7)
    time.sleep(0.5)
    ReleaseKey(number7)
    ReleaseKey(ctrl)

    PressKey(ctrl)
    PressKey(number6)
    time.sleep(0.5)
    ReleaseKey(number6)
    ReleaseKey(ctrl)

if __name__ == '__main__':
    time.sleep(5)
    time1 = time.time()
    while(True):
        if abs(time.time()-time1) > 5:
            break
        else:
            defense()

    Cheat()

    lock_vision()

    F_go()

    jump()