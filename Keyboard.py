import os
from cvzone.HandTrackingModule import HandDetector

import cv2
import numpy as np
import mediapipe as mp


import pyautogui

class Keys:
    def __init__(self) -> None:
        self.handDetector = HandDetector(detectionCon=0.8, maxHands=2)

        self.anim = [[]]
        self.animNum = -1
        self.animStart = False
        self.folderPath = "Images"

        self.pathImages = sorted(os.listdir(self.folderPath), key=len)

        self.cap = cv2.VideoCapture(0)

        #reader = LetterReader()

        self.imgNum = 0
        self.draw = True
        self.type = False

        self.showPic = False


    #Switches position on screen to letter value
    def getLetter(self, x, y):
        #DO TOP ROW
        if (x > 63 and x < 96) and (y < 115 and y > 76):
            return 'a'

        if (x > 111  and x < 157) and (y < 115 and y > 76):
            return 's'
        
        if (x > 175  and x < 217) and (y < 115 and y > 76):
            return 'd'
            
        if (x > 226  and x < 268) and (y < 115 and y > 76):
            return 'f'
        
        if (x > 285  and x < 330) and (y < 115 and y > 76):
            return 'g'

        if (x > 345  and x < 388) and (y < 115 and y > 76):
            return 'h'

        if (x > 403  and x < 454) and (y < 115 and y > 76):
            return 'j'

        if (x > 462  and x < 500) and (y < 115 and y > 76):
            return 'k'

        if (x > 518  and x < 562) and (y < 115 and y > 76):
            return 'l'

        if (x > 81  and x < 130) and (y < 173 and y > 127):
            return 'z'

        if (x > 141  and x < 191) and (y < 173 and y > 127):
            return 'x'

        if (x > 202  and x < 245) and (y < 173 and y > 127):
            return 'c'

        if (x > 271  and x < 307) and (y < 173 and y > 127):
            return 'v'
        
        if (x > 324  and x < 364) and (y < 173 and y > 127):
            return 'b'
        
        if (x > 374  and x < 429) and (y < 173 and y > 127):
            return 'n'

        if (x > 443  and x < 490) and (y < 173 and y > 127):
            return 'm'

        if (x > 38  and x < 83) and (y < 56 and y > 14):
            return 'q'

        if (x > 97  and x < 143) and (y < 56 and y > 14):
            return 'w'
        
        if (x > 155  and x < 200) and (y < 56 and y > 14):
            return 'e'
            
        if (x > 207  and x < 259) and (y < 56 and y > 14):
            return 'r'
        
        if (x > 273  and x < 320) and (y < 56 and y > 14):
            return 't'
        
        if (x > 324  and x < 369) and (y < 56 and y > 14):
            return 'y'
        
        if (x > 382  and x < 434) and (y < 56 and y > 14):
            return 'u'
        
        if (x > 439  and x < 482) and (y < 56 and y > 14):
            return 'i'
        
        if (x > 504  and x < 540) and (y < 56 and y > 14):
            return 'o'
        
        if (x > 556  and x < 605) and (y < 56 and y > 14):
            return 'p'
        return ''


    def run(self, img):
        # img = cap.read()
        # img = cv2.flip(img, 1)
        
        hands, img = self.handDetector.findHands(img)

        pathFullImage = os.path.join(self.folderPath, self.pathImages[self.imgNum])
        pic = cv2.imread(pathFullImage)

        if hands:
            hand = hands[0]
            fingers = self.handDetector.fingersUp(hand)
            points = hand["lmList"] 

            #Gets position of all finger tips
            thumbPos = points[4][0], points[4][1]
            indexPos = points[8][0], points[8][1]
            middlePos = points[12][0], points[12][1]
            ringPos = points[16][0], points[16][1]
            pinkiePos = points[20][0], points[20][0]

            #Other finger projects needed
            index2Pos = points[7][0], points[7][1]
            middle2Pos = points[11][0], points[11][1]

        
            
            #Keyboard cursor
            cv2.circle(pic, indexPos, 10, (0,0,255), cv2.FILLED)


            ### DRAWING FUNCTIONS ##########################

            #Switches to self.drawing board
            if fingers == [1, 0, 0, 0, 0]:
                if self.imgNum == 1:
                    self.imgNum = 0
                    self.animStart = False
                    self.anim.clear()
                    self.animNum = -1
                    self.anim.append([])
                    self.draw = True

            #Clears screen
            if fingers == [1, 1, 1, 1, 1] and self.draw:
                self.animStart = False
                self.anim.clear()
                self.animNum = -1
                self.anim.append([])

                #Draws on box screen
            if fingers == [0, 1, 0, 0, 0] and self.draw:
                if self.animStart is False:
                    self.animStart = True
                    self.animNum += 1
                    self.anim.append([])
                    #Appends a position of current index finger
                self.anim[self.animNum].append(indexPos)
                cv2.circle(pic, indexPos, 4, (0, 0, 255), cv2.FILLED)
            else:
                self.animStart = False

            
            ### KEYBOARD FUNCTIONS #############################

            #Switches screens to keyboard
            if fingers == [0, 0, 0, 0, 1]:
                if self.imgNum == 0:
                    self.imgNum = 1
                    self.animStart = False
                    self.anim.clear()
                    self.animNum = -1
                    self.anim.append([])
                    self.draw = False

            if fingers == [1, 1, 1, 1, 1] and self.draw == False:
                pyautogui.press("enter")

            if (middlePos[0] <= indexPos[0] and middlePos[1] >= indexPos[1]) and self.draw == False:
                if self.type is False:
                    pyautogui.press("backspace")
                    self.type = True
            else:
                self.type = False

            #Sends input for letter
            if fingers == [1, 1, 0, 0, 0] and self.draw == False: 
                if self.type is False:
                    self.type = True
                    pyautogui.write(self.getLetter(indexPos[0], indexPos[1]))
                    
            else:
                self.type = False

            #Sends input for uppercase letter
            if fingers == [1, 1, 1, 0, 0] and self.draw == False: 
                if self.type is False:
                    self.type = True
                    pyautogui.write(self.getLetter(indexPos[0], indexPos[1]).upper())

            #Writes a SPACE
            if fingers == [0, 1, 1, 1, 1,]:
                if self.type is False:
                    self.type = True
                    pyautogui.write(" ")
            else:
                self.type = False    
            
            if fingers == [1, 0, 0, 0, 1]:
                self.showPic = True
            else:
                self.showPic = False
        else:
            self.animStart = False

            
        for i, annotation in enumerate(self.anim):
            for j in range(len(annotation)):
                if j != 0:
                    cv2.line(pic, annotation[j - 1], annotation[j], (0, 0, 200), 12)

        
        cv2.imshow("Picture", pic)
        #cv2.imshow("Screen", img)
        
        key = cv2.waitKey(1)
