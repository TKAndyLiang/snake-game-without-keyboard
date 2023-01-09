import multiprocessing
import os
import time
import globals
import cv2
import mediapipe as mp
from utils import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-m', '--method', default='direct', dest='alg', help='Different methods', type=str)
parser.add_argument('-c', '--camera', default=0, type=int)
args = parser.parse_args()

TIMEOUT = 2



def camera():
    os.system('python ./camera.py')

def count():
    os.system('python ./sleep.py')

def detect():
    if args.alg == 'direct':
        os.system(f'python ./HandTrackModule_du_direct.py --camera {args.camera}')
    elif args.alg == 'model':
        os.system(f'python ./HandTrackModule_du.py --camera {args.camera}')

def rec():
    os.system('python ./receive_du.py')

def game():
    os.system('python ./snake.py')

if __name__ == '__main__':
    globals.init()

    p1 = multiprocessing.Process(target=rec)
    p1.start()

    p2 = multiprocessing.Process(target=detect)
    p2.start()

    p3 = multiprocessing.Process(target=game)
    p3.start()
    p3.join()

    #while True:
    #    if time.time() - start >= TIMEOUT:
    #        p1.terminate()
    #        p2.terminate()
    #        break
        
