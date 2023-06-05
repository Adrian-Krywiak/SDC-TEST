import pyautogui
import numpy as np

def capture_screen():
    screen = pyautogui.screenshot()
    frame = np.array(screen)
    return frame
