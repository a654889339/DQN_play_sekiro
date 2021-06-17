# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:10:06 2021

@author: pang
"""

import numpy as np
from grabscreen import grab_screen
import cv2
import time
import directkeys
from getkeys import key_check
import random
from DQN_tensorflow_gpu import DQN
import os
import pandas as pd
from restart import restart
import random
import tensorflow.compat.v1 as tf

def pause_game(paused):
    keys = key_check()
    if 'T' in keys:
        if paused:
            paused = False
            print('start game')
            time.sleep(1)
        else:
            paused = True
            print('pause game')
            time.sleep(1)
    if paused:
        print('paused')
        while True:
            keys = key_check()
            # pauses game and can get annoying.
            if 'T' in keys:
                if paused:
                    paused = False
                    print('start game')
                    time.sleep(1)
                    break
                else:
                    paused = True
                    time.sleep(1)
    return paused

def take_action(action):
    if action == 0:     # n_choose
        pass
    elif action == 1:   # j
        directkeys.attack()
    elif action == 2:   # k
        directkeys.jump()
    elif action == 3:   # m
        directkeys.define()
    elif action == 4:   # r
        directkeys.dodge()

def action_judge(boss_blood, next_boss_blood, self_blood, next_self_blood, stop, emergence_break):
    # get action reward
    # emergence_break is used to break down training
    # 用于防止出现意外紧急停止训练防止错误训练数据扰乱神经网络
    if next_self_blood < 3:     # self dead
        if emergence_break < 2:
            reward = -10
            done = 1
            stop = 0
            emergence_break += 1
            return reward, done, stop, emergence_break
        else:
            reward = -10
            done = 1
            stop = 0
            emergence_break = 100
            return reward, done, stop, emergence_break
    elif next_boss_blood - boss_blood > 15:   #boss dead
        if emergence_break < 2:
            reward = 20
            done = 0
            stop = 0
            emergence_break += 1
            return reward, done, stop, emergence_break
        else:
            reward = 20
            done = 0
            stop = 0
            emergence_break = 100
            return reward, done, stop, emergence_break
    else:
        self_blood_reward = 0
        boss_blood_reward = 0
        # print(next_self_blood - self_blood)
        # print(next_boss_blood - boss_blood)
        if next_self_blood - self_blood < -7:
            if stop == 0:
                self_blood_reward = -6
                stop = 1
                # 防止连续取帧时一直计算掉血
        else:
            stop = 0
        if next_boss_blood - boss_blood <= -3:
            boss_blood_reward = 4
        # print("self_blood_reward:    ",self_blood_reward)
        # print("boss_blood_reward:    ",boss_blood_reward)
        reward = self_blood_reward + boss_blood_reward
        done = 0
        emergence_break = 0
        return reward, done, stop, emergence_break
        

DQN_model_path = "model_gpu_5"
DQN_log_path = "logs_gpu/"
WIDTH = 96
HEIGHT = 88

action_size = 5
# action[n_choose,j,k,m,r]
# j-attack, k-jump, m-defense, r-dodge, n_choose-do nothing

paused = True
# used to stop training

if __name__ == '__main__':
    agent = DQN(WIDTH, HEIGHT, action_size, DQN_model_path, DQN_log_path)
    # DQN init
    paused = pause_game(paused)
    # paused at the begin
    screen_gray = cv2.cvtColor(grab_screen(directkeys.window_size),cv2.COLOR_BGR2GRAY)
    blood_window_gray = cv2.cvtColor(grab_screen(directkeys.blood_window),cv2.COLOR_BGR2GRAY)
    # collect station gray graph
    station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
    # change graph to WIDTH * HEIGHT for station input
    boss_blood = directkeys.boss_blood_count(blood_window_gray)
    self_blood = directkeys.self_blood_count(blood_window_gray)
    # count init blood
    target_step = 0
    # used to update target Q network
    done = 0
    total_reward = 0
    stop = 0    
    # 用于防止连续帧重复计算reward
    last_time = time.time()
    emergence_break = 0  
    while True:
        station = np.array(station).reshape(-1,HEIGHT,WIDTH,1)[0]
        # reshape station for tf input placeholder
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        # get the action by state
        action = agent.Choose_Action(station)
        take_action(action)
        # take station then the station change
        screen_gray = cv2.cvtColor(grab_screen(directkeys.window_size),cv2.COLOR_BGR2GRAY)
        # collect station gray graph
        blood_window_gray = cv2.cvtColor(grab_screen(blood_window),cv2.COLOR_BGR2GRAY)
        # collect blood gray graph for count self and boss blood
        next_station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
        next_station = np.array(next_station).reshape(-1,HEIGHT,WIDTH,1)[0]
        station = next_station
        next_boss_blood = directkeys.boss_blood_count(blood_window_gray)
        next_self_blood = directkeys.self_blood_count(blood_window_gray)
        reward, done, stop, emergence_break = action_judge(boss_blood, next_boss_blood,
                                                           self_blood, next_self_blood,
                                                           stop, emergence_break)
        # get action reward
        if emergence_break == 100:
            # emergence break , save model and paused
            # 遇到紧急情况，保存数据，并且暂停
            print("emergence_break")
            agent.save_model()
            paused = True
        keys = key_check()
        paused = pause_game(paused)
        if 'G' in keys:
            print('stop testing DQN')
            break
        if done == 1:
            restart()
        
        
            
            
            
            
            
        
        
    
    