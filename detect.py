import cv2
import numpy as np
import mediapipe as mp
import math
import os
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

names = os.listdir('./gen')
image = cv2.imread('./gen/0000.jpg')
DESIRED_WIDTH = image.shape[0]
DESIRED_HEIGHT = image.shape[1]


images = {name: cv2.imread('./gen/'+name) for name in names}
MULTI_TIME_xPoss = []
MULTI_TIME_yPoss = []
start = time.time()
with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.7) as hands:
    for name, image in images.items():
        results = hands.process(cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 1))

        #print(f'Handedness of {name}:')
        #print(results.multi_handedness)

        if not results.multi_hand_landmarks:
            continue
        # Draw hand landmarks of each hand.
        #print(f'Hand landmarks of {name}:')
        image_hight, image_width, _ = image.shape
        annotated_image = cv2.flip(image.copy(), 1)
        xPoss = []
        yPoss = []
        for hand_landmarks in results.multi_hand_landmarks:            
            for i, lm in enumerate(hand_landmarks.landmark):
                xPoss.append(lm.x * DESIRED_WIDTH)
                yPoss.append(lm.y * DESIRED_HEIGHT)
        
        MULTI_TIME_xPoss.append(xPoss)
        MULTI_TIME_yPoss.append(yPoss)
        

        #     # Print index finger tip coordinates.
        #     print(
        #         f'Index finger tip coordinate: (',
        #         f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
        #         f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_hight})'
        #     )
        #     mp_drawing.draw_landmarks(
        #         annotated_image,
        #         hand_landmarks,
        #         mp_hands.HAND_CONNECTIONS,
        #         mp_drawing_styles.get_default_hand_landmarks_style(),
        #         mp_drawing_styles.get_default_hand_connections_style())
        # resize(cv2.flip(annotated_image, 1))

MULTI_TIME_xPoss = np.asarray(MULTI_TIME_xPoss)
MULTI_TIME_yPoss = np.asarray(MULTI_TIME_yPoss)

#print(MULTI_TIME_xPoss)
#print(MULTI_TIME_yPoss)
print(time.time()-start)