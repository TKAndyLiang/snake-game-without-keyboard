import cv2
import mediapipe as mp
import time
import os
import numpy as np
import pyautogui
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
    duration = 0.15
    start = time.time()
    MultiTime_lm = []
    cap = cv2.VideoCapture(args.camera)
    detector = handDetector()
    direction_int = '4'
    if not os.path.exists('./done.txt'):
        f = open('./done.txt', 'w')
        f.close()
    while True:
        if time.time() - start >= duration:
            while not os.path.exists('./done.txt'):
                direction = '4'
                # print("FPS not ok")
                #start = time.time()
                #continue
            f = open('./done.txt','r')
            direction_int = f.readline()
            f.close()              
            # print("FPS OK")
            os.remove('./done.txt')
            f = open('./lm.txt', "w")
            # print(len(MultiTime_lm))
            f.write(str(len(MultiTime_lm))+'\n')
            f.write(str(MultiTime_lm))
            f.close()
            MultiTime_lm = []
            start = time.time()
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

        if direction_int == '0':
            direction = 'up'
        elif direction_int == '1':
            direction = 'down'
        elif direction_int == '2':
            direction = 'right'
        elif direction_int == '3':
            direction = 'left'
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
