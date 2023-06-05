import cv2
import numpy as np
import pyautogui
import pytesseract

# Define constants for speed limit sign detection
MIN_CONTOUR_AREA = 1000  # Minimum contour area for a valid speed limit sign
ASPECT_RATIO_THRESHOLD = 1.5  # Maximum allowed aspect ratio for a valid speed limit sign
DIGIT_ASCII_THRESHOLD = 20  # ASCII threshold for considering a character as a digit

def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (800, 600))
    normalized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    return normalized_frame

def detect_speed_limit_signs(frame, aspect_ratio):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred_frame, threshold1=30, threshold2=100)

    # Find contours in the edge image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process detected contours
    for contour in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.03, True)

        # Filter contours based on area and aspect ratio
        if len(approx) == 4 and cv2.contourArea(approx) > MIN_CONTOUR_AREA:
            x, y, w, h = cv2.boundingRect(approx)
            detected_aspect_ratio = float(w) / h

            # Compare the aspect ratio with the expected value
            if abs(detected_aspect_ratio - aspect_ratio) < 0.1:
                # Extract the region of interest (ROI) containing the sign
                roi = frame[y:y + h, x:x + w]

                # Preprocess the ROI for OCR
                processed_roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
                processed_roi = cv2.threshold(processed_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                # Apply OCR to extract the text from the sign
                text = pytesseract.image_to_string(processed_roi, config='--psm 10')
                # Check if the extracted text contains a number between 20 and 100
                if any(20 <= int(num) <= 100 for num in text.split() if num.isdigit()):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    print("Setting speed to : " + text)
                    break

    return frame

# Set the expected aspect ratio of the speed limit sign
aspect_ratio = 0.5947712418300654  # Update with the actual aspect ratio

# Set up OCR using PyTesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

while True:
    # Capture screen frame
    screen = pyautogui.screenshot()
    frame = np.array(screen)

    # Preprocess frame
    processed_frame = preprocess_frame(frame)

    # Detect speed limit signs
    detected_frame = detect_speed_limit_signs(processed_frame, aspect_ratio)

    # Display the processed frame
    cv2.imshow('Speed Limit Sign Detection', detected_frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources and close windows
cv2.destroyAllWindows()
