import numpy as np
import cv2 as cv
import face_alignment
from skimage import io
from pyautogui import press, typewrite, hotkey
import pyautogui
import scipy
import pickle
import torch
import torchvision
import torch.nn as nn
import os
import keyboard
import time

pyautogui.FAILSAFE = False


to_emoji = {
    0: ":laughing:",
    1: ":smiley:",
    2: ":face_with_raised_eyebrow:",
    3: ":nerd:",
    4: ":weary:"
}

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, face_detector="sfd", flip_input=False, device='cpu')


class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(136, 100),  # the "connections between" layers
            nn.Sigmoid(),
            nn.Linear(100, 50),
            nn.Sigmoid(),
            nn.Linear(50, 50),
            nn.Sigmoid(),
            nn.Linear(50, 25),
            nn.Sigmoid(),
            nn.Linear(25, 5)
            # nn.Softmax(dim=0)
        )

    def forward(self, x):
        flattened = self.flatten(x)
        prediction = self.layers(flattened)
        return prediction


model = torch.load("model/better_test_model.pth")

cycle_counter = 0

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv.flip(frame, 1)

    """
    if keyboard.is_pressed('a'):
        smile_preds = fa.get_landmarks(frame)[0]
        #smile = smile_preds
        data.append(smile_preds)
    """

    if cycle_counter >= 100:
        preds_pre = fa.get_landmarks(frame)
        if preds_pre is not None:
            preds = torch.Tensor(fa.get_landmarks(frame)[0]).flatten().unsqueeze(0)
            s = torch.nn.Softmax()

            predicted = s(model(preds))[0]
            amax = torch.argmax(predicted)
            print(predicted)
            if (predicted[amax] >= 0.75):
                typewrite(to_emoji[int(amax.item())])
                press("enter")

            cycle_counter = 0

    # Display the resulting frame
    cv.imshow('frame', frame)
    cycle_counter += 1

    if keyboard.is_pressed("H"):
        break

    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
os.system("python main.py")
