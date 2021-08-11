import cv2
from os import system

import numpy as np
from mss import mss
from PIL import Image

from utils import *
from sudoku_solution import Solution


mon = {'left': 150, 'top': 150, 'width': 1000, 'height': 800}

with mss() as sct:
    while True:

        screenShot = sct.grab(mon)
        img = np.array(Image.frombytes(
            'RGB', 
            (screenShot.width, screenShot.height), 
            screenShot.rgb,
        ))

        # img = cv2.imread("Images/fail0.png")

        HEIGHT, WIDTH = img.shape[:2]
        AREA = HEIGHT * WIDTH

        CELL_AREA_MAX = int(AREA / (9*9)) + 1
        CELL_AREA_MIN = CELL_AREA_MAX // 12



        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 4)
        thresh2 = cv2.erode(thresh, KERNEL5)



        contours, _ = cv2.findContours(thresh2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)



        possible_cell_area = []
        boards = []

        for cnt in contours:

            cur = cv2.contourArea(cnt)
            
            if CELL_AREA_MIN < cur < CELL_AREA_MAX:

                simplified = approxPoly(cnt)
                if len(simplified) == 4:
                    possible_cell_area.append(cur)
            
            elif CELL_AREA_MIN * 81 < cur < CELL_AREA_MAX * 81:
                
                simplified = approxPoly(cnt)
                if len(simplified) == 4:
                    boards.append([cur, simplified])


        possible_cell_area.sort()

        Area, _ = frameArea(possible_cell_area)

        if not Area:
            cv2.imshow("screen", img)
            if cv2.waitKey(33) & 0xFF in (ord('q'), 27):
                break
            continue


        outerContour = None

        for area, contour in boards:
            if Area < area < Area * 2:
                outerContour = contour


        if outerContour is not None:
            
            pt1 = np.float32(sorted(outerContour.reshape(4, 2), key=lambda x: (x[0], x[1])))
            
            pt2 = [[0, 0], [0, OUTER_DIM], [OUTER_DIM, 0], [OUTER_DIM, OUTER_DIM]]
            if pt1[0][1] > pt1[1][1]:
                pt2[0], pt2[1] = pt2[1], pt2[0]
            
            if pt1[2][1] > pt1[3][1]:
                pt2[2], pt2[3] = pt2[3], pt2[2]
            
            pt2 = np.float32(pt2)
            
            M = cv2.getPerspectiveTransform(pt1, pt2)
            new_img = cv2.warpPerspective(thresh, M, (OUTER_DIM, OUTER_DIM))
            new_img = cv2.bitwise_not(new_img)
            
        else:
            print("No board detected")
            cv2.imshow("screen", img)
            if cv2.waitKey(33) & 0xFF in (ord('q'), 27):
                break
            continue


        rois = []

        for i in range(9):
            rois.append([])
            for j in range(9):
                rois[-1].append(new_img[CELL*i + MARGIN:CELL*(i+1) - MARGIN, CELL*j + MARGIN: CELL*(j+1) - MARGIN])
                # cv2.imwrite(f"cells/img-{i}{j}.png", rois[-1][-1])


        unsolved_board = getSudokuboard(rois).tolist()

        solved_board = [[unsolved_board[i][j] for j in range(9)] for i in range(9)]
        Solution().solveSudoku(solved_board)

        print(unsolved_board)

        aug_text = np.zeros((OUTER_DIM, OUTER_DIM, 3), dtype=np.uint8)

        for x in range(9):
            for y in range(9):
                
                if unsolved_board[x][y] == 0:
                    loc = ((y) * CELL + MARGIN + 5, (x+1)*CELL - MARGIN - 3)
                    cv2.putText(aug_text, str(solved_board[x][y]), loc, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)


        # cv2.imshow("thresh", thresh)
        # if cv2.waitKey(33) & 0xFF in (ord('q'), 27):
        #     break


        M = cv2.getPerspectiveTransform(pt2, pt1)
        corrected_aug_text = cv2.warpPerspective(aug_text, M, (WIDTH, HEIGHT))


        mask = cv2.cvtColor(corrected_aug_text, cv2.COLOR_BGR2GRAY)

        _, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        fg = cv2.bitwise_and(corrected_aug_text, corrected_aug_text, mask=mask)
        bg = cv2.bitwise_and(img, img, mask=mask_inv)

        final_img = cv2.add(fg, bg)


        cv2.imshow("screen", final_img)
        if cv2.waitKey(33) & 0xFF in (ord('q'), 27):
            break


cv2.waitKey(0)
cv2.destroyAllWindows()