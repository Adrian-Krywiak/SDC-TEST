from road_detection.speed_limit_detection import detect_speed_limit_signs
from vision.screen_capture import capture_screen
from road_detection.lane_detection import detect_lanes
import cv2

while True:
    screen_capture = capture_screen()

    # Detect lanes
    lane_image = detect_lanes(screen_capture)

    if lane_image is not None:
        # Convert color space
        lane_image = cv2.cvtColor(lane_image, cv2.COLOR_BGR2RGB)

        # Display lane image
        cv2.imshow('Lane detection', lane_image)
    else:
        print("No lanes detected.")

    # Detect speed limit
    detected_speed = detect_speed_limit_signs(screen_capture)

    if detected_speed is not None:
        print("Detected speed: ", detected_speed)

    # Close the program if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
