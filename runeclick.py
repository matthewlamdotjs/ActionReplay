import time
from random import seed
from random import random
from pynput.mouse import Button, Controller
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from datetime import datetime

mouse = Controller()
seed(datetime.now())
delay = 2.09573123456

def click():
    (x, y) = mouse.position
    CGEventPost(0, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x,y), kCGMouseButtonLeft))
    time.sleep(0.03 + (random() * 0.1))
    CGEventPost(0, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x,y), kCGMouseButtonLeft))

def clickpos(coord):
    (x, y) = coord
    CGEventPost(0, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x,y), kCGMouseButtonLeft))
    time.sleep(0.03 + (random() * 0.1))
    CGEventPost(0, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x,y), kCGMouseButtonLeft))

def camelot():
    # higher frequency longer wait
    if(random() < 0.20):
        wait = delay + (random() * 1.5)
        print(wait)
        click()
        time.sleep(wait)
        if(random() < 0.02):
            print('random sleep')
            time.sleep(5 + (random() * 45))
    # lower frequency shorter wait
    else:
        wait = delay + (random() * 2.1)
        print(wait)
        click()
        time.sleep(wait)
        if(random() < 0.02):
            print('random sleep')
            time.sleep(5 + (random() * 10))
    # re seed?
    if(random() > 0.9):
        seed(datetime.now())

def alching():
    wait = 1.3 + (random() * 0.5)
    print(wait)
    click()
    time.sleep(wait)
    # re seed?
    if(random() > 0.9):
        seed(datetime.now())

def herblore():
    wait = 0.3 + (random() * 0.5)
    print(wait)
    click()
    time.sleep(wait)
    # re seed?
    if(random() > 0.9):
        seed(datetime.now())

def canafis():
    coords = [
        (1480, 634),
        (1624, 756),
        (1224, 760),
        (982, 870),
        (1022, 1168),
        (1362, 1144),
        (2182, 1720),
        (1662, 746)
    ]

    for coord in coords:
        time.sleep(5 + random())
        clickpos(coord)



# countdown to position
print('Starting in...')

for i in range(5):
    print(5 - i)
    time.sleep(1)

# loop paths
while(1):
    # camelot()
    # alching()
    # herblore()
    canafis()
    
