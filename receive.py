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
        len = int(fo.readline().strip('\n'))
        text = fo.read()
        fo.close()
        os.remove('./lm.txt')
        #text = fo.read().strip(']')
        all_text = ''.join([c for c in text if c not in ['[',']',',']]).split()
        all_int = list(map(int, all_text))
        #print(all_int)
        id_num = []
        if len == 0:
            fw = open('./done.txt','w')
            fw.write('4')
            fw.close()
            continue
        while all_int != []:
            x = all_int.pop(0)
            y = all_int.pop(0)
            id_num.append([x, y])
        #print(id_num)

        x_move_score = 0
        y_move_score = 0
        init_flag = False
        prev_x = [0] * 21
        prev_y = [0] * 21
        move_thre = 5
        n_right = 0
        n_left = 0
        n_up = 0
        n_down = 0
        id = 0
        #print(id_num)

        for x,y in id_num:
            if not init_flag:
                prev_x[id] = x
                prev_y[id] = y
            else:
                if x - prev_x[id] >= move_thre:
                    n_right += 1
                elif prev_x[id] - x >= move_thre:
                    n_left += 1

                if y - prev_y[id] >= move_thre:
                    n_down += 1
                elif prev_y[id] - y >= move_thre:
                    n_up += 1
                #print(prev_x[id]-x)

                prev_x[id] = x
                prev_y[id] = y
            
            id += 1
            #print(id)
            if id == 21:
                id = 0
                init_flag = True

        direction = [n_up, n_down, n_left, n_right]
        m = max(direction)
        out_direct = 4
        thre_frac = 0.3
        num_thre = int(len * 21 * thre_frac)

        if m >= num_thre:
            out_direct = direction.index(m)

        if out_direct == 0:
            pyautogui.press('up')
        elif out_direct == 1:
            pyautogui.press('down')
        elif out_direct == 2:
            pyautogui.press('right')
        elif out_direct == 3:
            pyautogui.press('left')

        fw = open('./done.txt','w')
        fw.write(str(out_direct))
        fw.close()
        #print(time.time() - start)
        #for i in range()
        # with io.open('./lm.txt','r',encoding='utf8') as f:
        #     text = f.read()
        #print(text)
    else:
        #print('wait data')
        time.sleep(0.1)