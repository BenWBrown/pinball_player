from pytesseract import image_to_string
from PIL import Image
import subprocess
import commands
import time
import autopy

pinball_location = "/Users/Ben/Applications/Wineskin/Pinball.app"
pinball_load_time = 5
newgame_time = 7
mouse_start = (450, 175)
mouse_end = (110, 30)

camtwist_location = "/Applications/CamTwist/CamTwist.app"
camtwist_load_time = 1

def score(frame, starting_pos):
    x, y = starting_pos
    ox, oy = 114, -187
    sx, sy = 155, 32
    return image_to_string(Image.fromarray(frame[y+oy:y+oy+sy, x+ox:x+ox+sx]))

def open_pinball():
    if not commands.getoutput('pgrep pinball'):
        subprocess.call(["/usr/bin/open", pinball_location])
        time.sleep(pinball_load_time)
        autopy.mouse.move(*mouse_start)
        time.sleep(.3)
        autopy.mouse.toggle(True)
        autopy.mouse.smooth_move(*mouse_end)
        autopy.mouse.toggle(False)

def new_game():
    autopy.key.tap(autopy.key.K_RETURN)
    time.sleep(.3)
    autopy.key.tap(autopy.key.K_F2)
    time.sleep(newgame_time)

def open_camtwist():
    subprocess.call(["/usr/bin/open", camtwist_location])
    time.sleep(camtwist_load_time)

def point_in_rect(point, rect):
    return rect[0][0] <= point[0] <= rect[1][0] and rect[0][1] <= point[1] <= rect[1][1]

def points_within_dist(p1, p2, d):
    return p1[0] - d <= p2[0] <= p1[0] + d and p1[1] - d <= p2[1] <= p1[1] + d
