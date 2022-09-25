import os
import keyboard
import time

while True:
    if keyboard.is_pressed("N"):
        os.system("python nickomode.py")
        time.sleep(0.1)
    elif keyboard.is_pressed("A"):
        os.system("python facial.py")
        time.sleep(0.1)
