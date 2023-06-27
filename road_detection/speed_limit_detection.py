import cv2
import pytesseract

# Define constants for speed limit sign detection
MIN_CONTOUR_AREA = 1000  # Minimum contour area for a valid speed limit sign
ASPECT_RATIO_THRESHOLD = 1.5  # Maximum allowed aspect ratio for a valid speed limit sign
DIGIT_ASCII_THRESHOLD = 20  # ASCII threshold for considering a character as a digit

def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (800, 600))
    normalized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    return normalized_frame

def detect_speed_limit_signs(frame):
    aspect_ratio = 0.5947712418300654  # Update with the actual aspect ratio
    # Set up OCR using PyTesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # Preprocess frame
    processed_frame = preprocess_frame(frame)

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2GRAY)

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
                roi = processed_frame[y:y + h, x:x + w]

                # Preprocess the ROI for OCR
                processed_roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
                processed_roi = cv2.threshold(processed_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                # Apply OCR to extract the text from the sign
                text = pytesseract.image_to_string(processed_roi, config='--psm 10')

                # Check if the extracted text contains a number between 20 and 100
                for num in text.split():
                    if num.isdigit() and 20 <= int(num) <= 100:
                        cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        return int(num)  # Return the detected speed immediately

                # If no speed limit is detected after going through the entire frame, return None
                return None