import cv2
import mediapipe as mp
import time
import pyautogui
import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import torch.nn.functional as F
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--camera', type=int, default=0)
args = parser.parse_args()

class MLP(nn.Module):
    def __init__(self, inc, outc):
        super(MLP, self).__init__()
        
        self.fc1 = nn.Linear(inc, 1024)
        self.fc2 = nn.Linear(1024, 2048)
        self.fc3 = nn.Linear(2048, 4096)
        self.classifier = nn.Sequential(    nn.Linear(4096, 1024),
                                            nn.ReLU(),
                                            nn.Linear(1024,outc))
        
        self.act = nn.ReLU()
    
    def forward(self, x):
        x = self.act(self.fc1(x))
        x = self.act(self.fc2(x))
        x = self.act(self.fc3(x))
        
        return self.classifier(x)

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
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = MLP(42,5)
    ckpt_temp = torch.load('./temp_3.pt')
    model.load_state_dict(ckpt_temp['model_state_dict'])
    model.eval()

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
        predict = 4
        if lmList != []:
            
            model_in = torch.FloatTensor(lmList).reshape(-1)
            predict = model(model_in)
            predict = torch.argmax(predict).item()

            detected = 1
            MultiTime_lm.append(lmList)
        # if len(lmList) != 0:
        #     print(lmList[4])
    

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        if not os.path.exists('./lm.txt'):
            f = open('./lm.txt', "w")
            f.write(str(predict))
            f.close()


        if predict == 0:
            direction = 'up'
            #pyautogui.press('up')
            #print("press up")
        elif predict == 1:
            direction = 'down'
            #pyautogui.press('down')
            #print("press down")
        elif predict == 2:
            direction = 'left'
            #pyautogui.press('left')
            #print("press left")
        elif predict == 3:
            direction = 'right'
            #pyautogui.press('right')
            #print("press right")
        else:
            direction = 'stay'
            #print("stay")

        cv2.putText(img, direction, (10, 170), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) == ord('x'):
            break
 
 
if __name__ == "__main__":
    main()
