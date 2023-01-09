import numpy as np
import cv2
import time
import os
import mediapipe as mp
import gc

def main():
    cap = cv2.VideoCapture(0)

    start = time.time()

    NUM_SAVE = 18 #+2 to true number
    SAVE_COUNT = 0
    Duration = 1

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    MULTI_TIME_xPoss = []
    MULTI_TIME_yPoss = []

    start = time.time()
    non_start_flag = False

    while True:
        start = time.time()
        #gc.collect()
        #if time.time() - start >= Duration and non_start_flag:
        #    MULTI_TIME_xPoss = np.asarray(MULTI_TIME_xPoss)
        #    MULTI_TIME_yPoss = np.asarray(MULTI_TIME_yPoss)
        #    print(MULTI_TIME_xPoss.shape)
        #    print(MULTI_TIME_yPoss.shape)
        #    MULTI_TIME_xPoss = []
        #    MULTI_TIME_yPoss = []
        #    start = time.time()
        #else:
        #    non_start_flag = True

        ret, frame = cap.read()

        #DESIRED_WIDTH = frame.shape[0]
        #DESIRED_HEIGHT = frame.shape[1]

        cv2.imshow('frame', frame)

        hands = mp_hands.Hands(False, 1, 1, 0.5, 0.5)
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        #print(f'Handedness of {name}:')
        #print(results.multi_handedness)

        if cv2.waitKey(1) == ord('x'):
            break

        print(1/(time.time()-start))

        #if not results.multi_hand_landmarks:
        #    continue
            # Draw hand landmarks of each hand.
            #print(f'Hand landmarks of {name}:')
            #image_hight, image_width, _ = image.shape
            #annotated_image = cv2.flip(image.copy(), 1)
        
        #xPoss = []
        #yPoss = []

        #for lm in results.multi_hand_landmarks[0].landmark:
        #    xPoss.append(lm.x)
        #    yPoss.append(lm.y)
            
        #MULTI_TIME_xPoss.append(xPoss)
        #MULTI_TIME_yPoss.append(yPoss)

        #MULTI_TIME_xPoss = np.asarray(MULTI_TIME_xPoss)
        #MULTI_TIME_yPoss = np.asarray(MULTI_TIME_yPoss)

        


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()