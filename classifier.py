import torch
import numpy as np
import cv2
import torch
import torchvision
import torch.nn as nn
import torchvision.transforms.functional as TF
from PIL import Image
import pyautogui

model = torchvision.models.resnet50(pretrained=True)
num_classes = 5
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)
model.load_state_dict(torch.load('last_weight_10.pth'))
model.cuda()

model.eval()
cap = cv2.VideoCapture(0)
counter = 0
frames = []
result_list = []
true_dir = 2

while cap.isOpened():
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = TF.to_tensor(img)
    img = TF.resize(img, [224, 224]).cuda()

    # img = TF.resize(img, [224, 224]).cuda().unsqueeze(0)
    # result = model(img)
    # result = torch.argmax(result).detach().cpu()
    # result_list.append(result)

    # counter += 1
    # if counter % 10 == 0:
    #     print(result_list)
    #     counter = 0
    #     result_list = []

    frames.append(img)
    counter += 1
    if counter % 5 == 0:
        frames = torch.stack(frames, 0)
        results = model(frames)
        _, pred = torch.max(results, dim=1)
        # print(pred.detach().cpu().numpy())
        pred = pred.detach().cpu().numpy()
        true_dir = np.argmax(np.bincount(pred))
        pred_list = np.bincount(pred)
        if pred_list[true_dir] < 3:
            true_dir = 2

        print(true_dir)
        
        if true_dir == 4:
            pyautogui.press('up')
        elif true_dir == 0:
            pyautogui.press('down')
        elif true_dir == 1:
            pyautogui.press('left')
        elif true_dir == 3:
            pyautogui.press('right')
        else:
            direction = 'stay'

        counter = 0
        frames = []
        true_dir = 2


    cv2.imshow('hand', np.squeeze(frame))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
