import cv2

def extraction1(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter for noise reduction
    blur = cv2.bilateralFilter(gray, 11, 90, 90)

    # Apply adaptive thresholding
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    # Initialize plate variable
    plate = None

    # Iterate through contours
    for cnt in contours:
        # Approximate polygonal curves
        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Check if contour has 4 edges (likely a plate)
        if len(approx) == 4:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(cnt)
            plate = image[y:y + h, x:x + w]
            break

    return plate
