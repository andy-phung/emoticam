import os
import keyboard
import time

switch = 0

def check_start():
    start = 0
    if keyboard.is_pressed("N") and start == 0:
        os.system("python nickomode.py")
        time.sleep(0.1)
    if keyboard.is_pressed("A") and start == 1:
        os.system("python facial.py")
        time.sleep(0.1)


while True:
    check_start()
