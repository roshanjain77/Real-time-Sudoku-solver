import cv2
import time
import numpy as np
from keras.models import load_model
from tensorflow.keras.utils import normalize

from copy import deepcopy


MARGIN = 4
CELL = 28 + 2 * MARGIN
OUTER_DIM = 9 * CELL


KERNEL3 = np.ones((3, 3), np.uint8)
KERNEL5 = np.ones((5, 5), np.uint8)
KERNEL7 = np.ones((7, 7), np.uint8)


model = load_model('../Keras-Models/CNN+BN+DA-2')
model2 = load_model('../Keras-Models/digit_model.h5')


def getSudokuboard(rois):

    data = np.array(rois).reshape(-1, 28, 28, 1)

    data = data/255.0
    data2 = deepcopy(data)

    preds = model.predict(data)
    preds2 = model2.predict(data2)
    
    board = np.argmax(preds, axis=1).reshape(9, 9)
    board2 = np.argmax(preds2, axis=1).reshape(9, 9)

    for i in range(9):
        for j in range(9):
            if board[i][j] == 7 and board2[i][j] == 1:
                board[i][j] = 1
    
    return board


def done():
    key = cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()
    
    return key == 27


def show(*args):
    
    for arg in args:
        cv2.imshow(f"img-{time.time()}", arg)
        
    return done()


def showw(*args):
    
    for arg in args:
        cv2.imshow(f"img-{time.time()}", arg)
        

def draw_on(img, cnt, color='g', thickness=2):

    col = (0, 255, 0)
    
    if color == 'r':
        col = (0, 0, 255)
    elif color == 'b':
        col = (255, 0, 0)
    
    cv2.drawContours(img, cnt, -1, col, thickness)


        
def draw(img, cnt, color='g', thickness=2):
    
    new_img = img.copy()
    draw_on(new_img, cnt, color=color, thickness=thickness)
    
    return new_img
    

def approxPoly(cnt, factor=0.05):
    
    perimeter = cv2.arcLength(cnt, True)
    return cv2.approxPolyDP(cnt, factor*perimeter, True)


def frameArea(area):
    Area = None
    
    loc = 0

    if len(area) >= 81:

        minDiff = float('inf')

        for i in range(len(area) - 81 + 1):
            j = i + 81 - 1
            if minDiff > area[j]-area[i]:
                minDiff = area[j]-area[i]
                loc = i

        Area = sum(area[i:i+81])

    elif len(area) >= 25:
        Area = sum(area)/len(area)*81
        
    
        
    return Area, loc

x = cv2.imread('cells/img-11.png', 0)
rois = [[x for i in range(9)] for i in range(9)]

board = getSudokuboard(rois)
print(board)


cv2.imshow("one", rois[0][0])
cv2.waitKey(0)
cv2.destroyAllWindows()