import multiprocessing
import pyautogui
import io
import os
import time


#start = time.time()
while True:
    if os.path.exists('./lm.txt'):
        len_flag = True
        fo = open('./lm.txt','r')
        predict = fo.read()
        fo.close()
        os.remove('./lm.txt')
        #text = fo.read().strip(']')
        if predict == '0':
            pyautogui.press('up')
            #print("press up")
        elif predict == '1':
            pyautogui.press('down')
            #print("press down")
        elif predict == '2':
            pyautogui.press('left')
            #print("press left")
        elif predict == '3':
            pyautogui.press('right')
            #print("press right")
        #print(time.time() - start)
        #for i in range()
        # with io.open('./lm.txt','r',encoding='utf8') as f:
        #     text = f.read()
        #print(text)
    else:
        #print('wait data')
        time.sleep(0.1)