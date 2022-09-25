import os
import keyboard
import time
import subprocess

while True:
    if keyboard.is_pressed("n"):
        process = subprocess.Popen(["python3", "nickomode.py"])
        #os.system("python nickomode.py")
        time.sleep(0.1)
        if keyboard.wait("esc"):
            process.kill()
    elif keyboard.is_pressed("a"):
        #os.system("python facial.py")
        process = subprocess.Popen(["python3", "facial.py"])
        time.sleep(0.1)
        if keyboard.wait("esc"):
            process.kill()
