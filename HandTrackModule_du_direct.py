import cv2
import mediapipe as mp
import time
import pyautogui
import os
import numpy as np
import argparse

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
    duration = 0.3
    start = time.time()
    MultiTime_lm = []
    cap = cv2.VideoCapture(args.camera)
    detector = handDetector()
    direction_int = '4'
    if(not os.path.exists('./done.txt')):
        f = open('./done.txt','w')
        f.close()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        detected = 0
        direction_int = 4
        if lmList != []:
            detected = 1
            MultiTime_lm.append(lmList)
        # if len(lmList) != 0:
        #     print(lmList[4])
        if detected:
            distance_tip_to_bottom_x = lmList[8][0] - lmList[0][0]
            distance_tip_to_bottom_y = lmList[8][1] - lmList[0][1]
            distance_middle_to_bottom_x = lmList[6][0] - lmList[0][0]
            distance_middle_to_bottom_y = lmList[6][1] - lmList[0][1]
            distance_tip_to_middle_x = lmList[8][0] - lmList[5][0]
            distance_tip_to_middle_y = lmList[8][1] - lmList[5][1]
            if abs(distance_tip_to_bottom_x) + abs(distance_tip_to_bottom_y) > 1*abs(distance_middle_to_bottom_x) + 1*abs(distance_middle_to_bottom_y):
                if distance_tip_to_middle_x > 0:
                    if abs(distance_tip_to_middle_y) > abs(distance_tip_to_middle_x):
                        if distance_tip_to_middle_y > 0:
                            #pyautogui.press('down')
                            direction_int = 1
                            #print("press down")
                        else:
                            #pyautogui.press('up')
                            direction_int = 0
                            #print("press up")
                    else:
                        #pyautogui.press('left')
                        direction_int = 2
                        #print("press left")
                else:
                    if abs(distance_tip_to_middle_y) > abs(distance_tip_to_middle_x):
                        if distance_tip_to_middle_y > 0:
                            #pyautogui.press('down')
                            direction_int = 1
                            #print("press down")
                        else:
                            #pyautogui.press('up')
                            direction_int = 0
                            #print("press up")
                    else:
                        #pyautogui.press('right')
                        direction_int = 3
                        #print("press right")
            else:
                direction_int = 4
                #print("stay")
        
        if not os.path.exists('./lm.txt'):
            f = open('./lm.txt', "w")
            f.write(str(direction_int))
            f.close()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        if direction_int == 0:
            direction = 'up'
        elif direction_int == 1:
            direction = 'down'
        elif direction_int == 2:
            direction = 'left'
        elif direction_int == 3:
            direction = 'right'
        else:
            direction = 'stay'

        cv2.putText(img, direction, (10, 170), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) == ord('x'):
            break
 
 
if __name__ == "__main__":
    main()
