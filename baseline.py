import numpy as np
import cv2
import time
import keypress
import utils

timeout = 120
THRESHOLD = 0.075 #anything below this threshold is considered a match
#TODO: MOVE THIS TO SOME SORT OF UTILS LIBRARY


utils.open_camtwist()
utils.open_pinball()
utils.new_game()
print "game started"


##using CamTwist to create a virtual webcam this captures the screen.. I should
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

print "starting location: " + str(starting_pos)
start_time = time.time()
end_frame = None

while(True):
    t = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ret, frame = cap.read()
    if start_time + timeout < t:
        print "time"
        score = utils.score(frame, starting_pos) #todo: divide by number of balls used
        print score
        break

    res = cv2.matchTemplate(frame, ball, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if utils.points_within_dist(min_loc, starting_pos, 5):
        keypress.tap(" ", 2)

    col1 = (255, 0, 255) if utils.point_in_rect(min_loc, (rect11, rect12)) and min_val < THRESHOLD else (0, 255, 255)
    col2 = (255, 0, 0) if utils.point_in_rect(min_loc, (rect21, rect22)) and min_val < THRESHOLD else (0, 255, 0)

    if utils.point_in_rect(min_loc, (rect11, rect12)) and min_val < THRESHOLD:
        keypress.tap('/')
    if utils.point_in_rect(min_loc, (rect21, rect22)) and min_val < THRESHOLD:
        keypress.tap('z')

    # cv2.rectangle(frame, rect11, rect12, col1)
    # cv2.rectangle(frame, rect21, rect22, col2)
    # cv2.circle(frame, (starting_pos[0] + 3, starting_pos[1] + 3), 5, (0, 0, 255), 3 )
    #
    #
    # cv2.imshow('frame',frame)



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
