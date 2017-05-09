import numpy as np
import cv2
import time
import keypress
import utils

THRESHOLD = 0.075 #anything below this threshold is considered a match
#TODO: MOVE THIS TO SOME SORT OF UTILS LIBRARY

def point_in_rect(point, rect):
    return rect[0][0] <= point[0] <= rect[1][0] and rect[0][1] <= point[1] <= rect[1][1]

##using CamTwist to create a virtual webcam this captures the screen.. I should
##probably have it capture only part of the screen
cap = cv2.VideoCapture(0)

ball = cv2.imread('ball.png', 1)
radius = ball.shape[0] / 2

pos = 0.0, 0.0
velocity = 0.0, 0.0

time.sleep(2)
ret, frame = cap.read()

res = cv2.matchTemplate(frame, ball, cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

starting_pos = min_loc


offset1 = -140, -10
offset2 = -190, -10
size = 40, 40

rect11 = tuple([x + y for x,y in zip(starting_pos, offset1)])
rect12 = tuple([x + y for x,y in zip(rect11, size)])

rect21 = tuple([x + y for x,y in zip(starting_pos, offset2)])
rect22 = tuple([x + y for x,y in zip(rect21, size)])

while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ret, frame = cap.read()

    res = cv2.matchTemplate(frame, ball, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    col1 = (255, 0, 255) if point_in_rect(min_loc, (rect11, rect12)) and min_val < THRESHOLD else (0, 255, 255)
    col2 = (255, 0, 0) if point_in_rect(min_loc, (rect21, rect22)) and min_val < THRESHOLD else (0, 255, 0)

    if point_in_rect(min_loc, (rect11, rect12)) and min_val < THRESHOLD:
        keypress.tap('/')
    if point_in_rect(min_loc, (rect21, rect22)) and min_val < THRESHOLD:
        keypress.tap('z')

    cv2.rectangle(frame, rect11, rect12, col1)
    cv2.rectangle(frame, rect21, rect22, col2)
    cv2.circle(frame, (starting_pos[0] + 3, starting_pos[1] + 3), 5, (0, 0, 255), 3 )


    cv2.imshow('frame',frame)



while(False):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Apply template Matching
    res = cv2.matchTemplate(frame, ball, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # print min_val, min_loc, max_val, max_loc
    if min_val < THRESHOLD:
        cv2.circle(frame, (min_loc[0] + radius, min_loc[1] + radius), radius + 2, (0, 0, 255), 3 )

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
