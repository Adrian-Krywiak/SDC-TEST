from road_detection.speed_limit_detection import detect_speed_limit_signs
from vision.screen_capture import capture_screen

# Speed limit detection
#_______________________________________________________________________________________________________________________________________________________________________________________
while True:
    detected_speed = detect_speed_limit_signs(capture_screen)
    if detected_speed is not None:
        print("Detected speed: ", detected_speed)
        # Once I have the car controls build i can control it here
        # For now I will just print the speed
#_______________________________________________________________________________________________________________________________________________________________________________________

