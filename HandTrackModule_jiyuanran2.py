import cv2
import mediapipe as mp
import time
import os
import numpy as np
import pyautogui

parser = argparse.ArgumentParser()
parser.add_argument('--camera', type=int, default=0)
args = parser.parse_args()
 
class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplexity = modelComplexity
 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
 
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
 
    def findPosition(self, img, handNo=0, draw=True):
 
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
 
        return lmList

def main():
    pTime = 0
    cTime = 0
    duration = 0.15
    start = time.time()
    MultiTime_lm = []
    cap = cv2.VideoCapture(args.camera)
    detector = handDetector()
    direction = 4
    show_direction = ['up', 'down', 'right', 'left', 'stay']
    while True:
        if time.time() - start >= duration:
            if MultiTime_lm == []:
                start = time.time()
            else:
                t = len(MultiTime_lm)
                print(t)
                init_flag = False
                prev_x = [0] * 21
                prev_y = [0] * 21
                move_thre = 5
                n_right = 0
                n_left = 0
                n_up = 0
                n_down = 0
                #MultiTime_lm => (t, 21, x, y)

                for i in range(t):
                    for id in range(21):
                        x = MultiTime_lm[i][id][0]
                        y = MultiTime_lm[i][id][1]
                        if not init_flag:
                            prev_x[id] = x
                            prev_y[id] = y
                        else:
                            if x - prev_x[id] >= move_thre:
                                n_left += 1
                            elif prev_x[id] - x >= move_thre:
                                n_right += 1

                            if y - prev_y[id] >= move_thre:
                                n_down += 1
                            elif prev_y[id] - y >= move_thre:
                                n_up += 1
                            #print(prev_x[id]-x)

                            prev_x[id] = x
                            prev_y[id] = y
                
                        #print(id)
                        if id == 20:
                            id = 0
                            init_flag = True

                directions = [n_up, n_down, n_right, n_left]
                m = max(directions)
                out_direct = 4
                thre_frac = 0.3
                num_thre = int(t * 21 * thre_frac)

                if m >= num_thre:
                    out_direct = directions.index(m)

                if out_direct == 0:
                    pyautogui.press('up')
                elif out_direct == 1:
                    pyautogui.press('down')
                elif out_direct == 2:
                    pyautogui.press('right')
                elif out_direct == 3:
                    pyautogui.press('left')

                MultiTime_lm = []
                start = time.time()
                direction = out_direct
        else:
            direction = 4

        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList != []:
            MultiTime_lm.append(lmList)
        # if len(lmList) != 0:
        #     print(lmList[4])
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.putText(img, show_direction[direction], (10, 170), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) == ord('x'):
            break
 
 
if __name__ == "__main__":
    main()
